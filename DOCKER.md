# Docker

```powershell
copy server\.env.example server\.env
docker compose up -d --build
```

Open:

```text
Frontend: http://localhost:5173
Backend API: http://localhost:8000
Swagger: http://localhost:8000/docs
Health: http://localhost:8000/api/v1/health/
```

To run the Telegram bot

```powershell
docker compose --profile bot up -d --build
```

