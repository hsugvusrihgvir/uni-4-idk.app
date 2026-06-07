# idk.app

Веб-приложение для брейншторма: команды создают доски, собирают идеи, модерируют предложения, голосуют и сохраняют лучшие варианты в отчёт.


- регистрация и вход по email-коду;
- создание досок для брейншторма;
- добавление и поиск идей;
- модерация идей перед публикацией;
- роли участников: пользователь, модератор, администратор;
- управление участниками доски;
- голосования по идеям и просмотр результатов;
- уведомления о событиях на досках;
- профиль пользователя и привязка Telegram-аккаунта;
- добавление идей через Telegram-бота;
- экспорт отобранных идей в HTML-отчёт.

## Технологии

Frontend: Vue 3, Vite, Vitest  
Backend: FastAPI, SQLAlchemy, PostgreSQL  
Auth: JWT access/refresh tokens  
Integrations: email-коды, Telegram bot  

## Быстрый запуск через Docker

```powershell
copy server\.env.example server\.env
docker compose up -d --build
```

После запуска:

- приложение: http://localhost:5173
- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- healthcheck: http://localhost:8000/api/v1/health/

Остановить контейнеры:

```powershell
docker compose down
```

## Переменные окружения

Основной пример лежит в `server/.env.example`.


## Telegram-бот

чтобы участники могли добавлять идеи прямо из Telegram-чата

Запуск вместе с приложением:

```powershell
docker compose --profile bot up -d --build
```

Как работает сценарий:

1. пользователь получает код привязки в профиле;
2. отправляет боту `/link код`;
3. администратор добавляет бота в чат и выполняет `/bind id_доски`;
4. участники отправляют идеи командой `/idea текст идеи`;
5. идея попадает на доску или на модерацию.


## Проверка

Backend-тесты:

```powershell
python -m pytest server/tests
```

Frontend-тесты:

```powershell
cd client
npm run test
```
