import asyncio
import os
from pathlib import Path
from uuid import UUID, uuid4

import httpx
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandObject
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
BOT_SECRET = os.getenv("TELEGRAM_BOT_SECRET")
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

dp = Dispatcher()
pending_ideas: dict[str, dict] = {}


def api_headers() -> dict:
    return {"X-Bot-Secret": BOT_SECRET or ""}


async def api_post(path: str, payload: dict) -> dict:
    async with httpx.AsyncClient(timeout=20) as client:
        response = await client.post(f"{API_URL}{path}", json=payload, headers=api_headers())

    data = response.json() if response.content else {}
    if response.status_code >= 400:
        raise ValueError(data.get("detail", "ошибка"))

    return data


def idea_keyboard(token: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="сохранить", callback_data=f"idea:save:{token}"),
                InlineKeyboardButton(text="отмена", callback_data=f"idea:cancel:{token}"),
            ]
        ]
    )


@dp.message(Command("start", "help"))
async def help_message(message: Message) -> None:
    await message.answer(
        "привет. я бот для идей с доски.\n\n"
        "как начать:\n"
        "1. на сайте открой профиль и получи код telegram\n"
        "2. напиши мне в личку /link код\n"
        "3. добавь меня в общий чат\n"
        "4. админ доски пишет в чате /bind id_доски\n"
        "5. потом можно писать /idea текст идеи\n\n"
        "после /idea я попрошу подтвердить сохранение кнопкой."
    )


@dp.message(Command("link"))
async def link_user(message: Message, command: CommandObject) -> None:
    code = (command.args or "").strip()

    if message.chat.type != "private":
        await message.answer("код лучше писать мне в личку, не в общий чат")
        return

    if not code:
        await message.answer("напиши так: /link 123456")
        return

    try:
        await api_post(
            "/api/v1/telegram/users/link",
            {
                "code": code,
                "telegram_user_id": message.from_user.id,
            },
        )
    except ValueError as e:
        await message.answer(str(e))
        return
    except httpx.HTTPError:
        await message.answer("не получилось связаться с сервером")
        return

    await message.answer("готово, тг привязан к аккаунту")


@dp.message(Command("bind"))
async def bind_chat(message: Message, command: CommandObject) -> None:
    board_id = (command.args or "").strip()

    if message.chat.type == "private":
        await message.answer("эту команду надо писать в общем чате")
        return

    try:
        UUID(board_id)
    except ValueError:
        await message.answer("напиши так: /bind uuid_доски")
        return

    try:
        await api_post(
            "/api/v1/telegram/chats/bind",
            {
                "board_id": board_id,
                "telegram_user_id": message.from_user.id,
                "telegram_chat_id": message.chat.id,
                "chat_title": message.chat.title,
            },
        )
    except ValueError as e:
        await message.answer(str(e))
        return
    except httpx.HTTPError:
        await message.answer("не получилось связаться с сервером")
        return

    await message.answer("готово, этот чат привязан к доске")


@dp.message(Command("idea"))
async def prepare_idea(message: Message, command: CommandObject) -> None:
    text = (command.args or "").strip()

    if not text:
        await message.answer("напиши так: /idea текст идеи")
        return

    token = uuid4().hex
    pending_ideas[token] = {
        "telegram_user_id": message.from_user.id,
        "telegram_chat_id": message.chat.id,
        "text": text,
        "author_id": message.from_user.id,
    }

    await message.answer(f"сохранить идею?\n\n{text}", reply_markup=idea_keyboard(token))


@dp.callback_query(F.data.startswith("idea:cancel:"))
async def cancel_idea(callback: CallbackQuery) -> None:
    token = callback.data.rsplit(":", 1)[-1]
    payload = pending_ideas.get(token)

    if payload and payload["author_id"] != callback.from_user.id:
        await callback.answer("это может отменить только автор идеи", show_alert=True)
        return

    pending_ideas.pop(token, None)
    await callback.message.edit_text("ок, не сохраняю")
    await callback.answer()


@dp.callback_query(F.data.startswith("idea:save:"))
async def save_idea(callback: CallbackQuery) -> None:
    token = callback.data.rsplit(":", 1)[-1]
    payload = pending_ideas.pop(token, None)

    if payload is None:
        await callback.answer("идея уже обработана", show_alert=True)
        return

    if payload["author_id"] != callback.from_user.id:
        pending_ideas[token] = payload
        await callback.answer("это может сохранить только автор идеи", show_alert=True)
        return

    payload = {
        "telegram_user_id": payload["telegram_user_id"],
        "telegram_chat_id": payload["telegram_chat_id"],
        "text": payload["text"],
    }

    try:
        idea = await api_post("/api/v1/telegram/ideas", payload)
    except ValueError as e:
        await callback.message.edit_text(str(e))
        await callback.answer()
        return
    except httpx.HTTPError:
        await callback.message.edit_text("не получилось связаться с сервером")
        await callback.answer()
        return

    status = "на модерации" if idea.get("status") == "pending" else "опубликована"
    await callback.message.edit_text(f"идея добавлена: {status}")
    await callback.answer()


async def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN is not set")
    if not BOT_SECRET:
        raise RuntimeError("TELEGRAM_BOT_SECRET is not set")

    bot = Bot(BOT_TOKEN)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
