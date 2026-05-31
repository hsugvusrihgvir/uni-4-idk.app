# idk.app

Курсовая работа, 4 семестр

Веб-приложение для сбора, модерации и отбора идей на досках. Пользователи могут создавать доски, добавлять идеи, участвовать в голосованиях и получать уведомления. Для администраторов и модераторов доступны управление участниками, настройками доски и статусами идей.

## Стек

- Frontend: Vue 3, Vite, Vitest
- Backend: FastAPI, SQLAlchemy, PostgreSQL
- Авторизация: JWT access/refresh tokens
- Дополнительно: Telegram-бот для привязки аккаунта и добавления идей из чата

## Структура проекта

```text
client/   frontend-приложение
server/   backend-приложение
```

## Переменные окружения

Для backend в папке `server` нужен файл `.env`.

Пример:

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=postgres
DB_PASSWORD=postgres
DB_NAME=idk_app

SECRET_KEY=change_me
API_URL=http://127.0.0.1:8000

TELEGRAM_BOT_TOKEN=
TELEGRAM_BOT_SECRET=change_me

MAIL_USERNAME=
MAIL_KEY=
MAIL_FROM=
SMTP_HOST=smtp.mail.ru
SMTP_PORT=465
```

## Запуск backend

```powershell
cd server
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API будет доступно по адресу:

```text
http://127.0.0.1:8000
```

Swagger-документация:

```text
http://127.0.0.1:8000/docs
```

## Запуск frontend

```powershell
cd client
npm install
npm run dev
```

Frontend обычно открывается по адресу:

```text
http://127.0.0.1:5173
```

## Запуск Telegram-бота

Сначала нужно указать `TELEGRAM_BOT_TOKEN` и `TELEGRAM_BOT_SECRET` в `server/.env`.

```powershell
cd server
python -m app.bot.telegram_bot
```

## Тесты backend

```powershell
python -m pytest server/tests
```

Проверяются основные API-сценарии: авторизация, профиль, доски, идеи, голосования и результаты.

## Тесты frontend

```powershell
cd client
npm run test
```

Проверяются HTTP-клиент, запросы к API и обработка ошибок в store.

## Сборка frontend

```powershell
cd client
npm run build
```

Готовая сборка появляется в папке `client/dist`.
