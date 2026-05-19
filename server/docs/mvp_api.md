# MVP

## 1) auth

### 1.1 `POST /api/v1/auth/login`
**Кто:** Гость  
отправить email, проверить есть ли аккаунт

**Body:**
```json
{
  "email": "user@example.com"
}
```

**Ответ (если есть аккаунт):**
```json
{
  "exists": true,
  "message": "Код отправлен в Telegram"
}
```

**Ответ (если нет аккаунта):**
```json
{
  "exists": false,
  "message": "Аккаунт не найден"
}
```

---

### 1.2 `POST /api/v1/auth/register`
**Кто:** Гость  
создать аккаунт и отправить код

**Body:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "name": "Name",
  "photo_url": "photo.png"
}
```

**Ответ:**
```json
{
  "message": "Код отправлен в Telegram"
}
```

---

### 1.3 `POST /api/v1/auth/verify`
**Кто:** Гость  
подтвердить код

**Body:**
```json
{
  "email": "user@example.com",
  "code": "123456"
}
```

**Ответ:**
```json
{
  "access_token": "jwt_token",
  "refresh_token": "refresh_token",
  "token_type": "bearer"
}
```

---

### 1.4 `POST /api/v1/auth/refresh`
**Кто:** Пользователь  
получить новый access-токен

**Body:**
```json
{
  "refresh_token": "refresh_token"
}
```

**Ответ:**
```json
{
  "access_token": "new_jwt_token",
  "token_type": "bearer"
}
```

---

## 2) Users

### 2.1 `GET /api/v1/users/check-username?username=rin`
**Кто:** Гость  
проверить username на существование

**Ответ:**
```json
{
  "available": false,
  "message": "Username уже занят"
}
```

или

```json
{
  "available": true,
  "message": "Username доступен"
}
```

---

### 2.2 `GET /api/v1/users/me`
**Кто:** Пользователь

**Ответ:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "name": "Name",
  "photo_url": "photo.png"
}
```

---

### 2.3 `PATCH /api/v1/users/me`
**Кто:** Пользователь

**Body:**
```json
{
  "username": "username",
  "name": "Name",
  "photo_url": "photo.png"
}
```

**Ответ:**
```json
{
  "email": "user@example.com",
  "username": "username",
  "name": "Name",
  "photo_url": "photo.png"
}
```

---

## 3) Boards

### 3.1 `POST /api/v1/boards`
**Кто:** Пользователь  
создать доску

**Body:**
```json
{
  "title": "Title",
  "description": "description",
  "moderation": false,
  "anon_ideas": true
}
```

**Ответ:**
```json
{
  "id": "uuid",
  "title": "Title",
  "description": "description",
  "moderation": false,
  "anon_ideas": true
}
```

---

### 3.2 `GET /api/v1/boards`
**Кто:** Пользователь  
получить список моих досок

**Ответ:**
```json
{
  "items": [
    {
      "id": "uuid",
      "title": "Board 1",
      "description": "description",
      "role": "admin"
    }
  ]
}
```

---

### 3.3 `GET /api/v1/boards/{board_id}`
**Кто:** Пользователь доски  
получить конкретную доску, идеи и мою роль

**Ответ:**
```json
{
  "id": "uuid",
  "title": "Board 1",
  "description": "description",
  "role": "admin",
  "anon_ideas": true,
  "moderation": false,
  "created_at": "01.01.2000",
  "ideas": [
    {
      "id": "uuid",
      "title": "Idea 1",
      "description": "description",
      "status": "approved"
    }
  ]
}
```

---

## 4) Ideas

### 4.1 `POST /api/v1/ideas`
**Кто:** Пользователь доски  
добавить идею

**Body:**
```json
{
  "board_id": "uuid",
  "title": "Title",
  "description": "description",
  "is_anonymous": true
}
```

**Ответ:**
```json
{
  "id": "uuid",
  "board_id": "uuid",
  "title": "Title",
  "description": "description",
  "status": "pending",
  "is_anonymous": true,
  "created_at": "01.01.2000"
}
```

---

### 4.2 `GET /api/v1/boards/{board_id}/ideas`
**Кто:** Пользователь доски  
получить список идей доски

**Ответ:**
```json
{
  "items": [
    {
      "id": "uuid",
      "title": "Idea 1",
      "description": "description",
      "status": "approved",
      "is_anonymous": true,
      "created_at": "01.01.2000"
    }
  ]
}
```

---

### 4.3 `WS /api/v1/boards/{board_id}/ideas/ws`
**Кто:** Пользователь доски  
получать идеи в реальном времени

**Сообщение при новой идее:**
```json
{
  "type": "idea_created",
  "idea": {
    "id": "uuid",
    "title": "Idea 1",
    "description": "description",
    "status": "approved",
    "is_anonymous": true,
    "created_at": "01.01.2000"
  }
}
```

---

## 5) Administration

### 5.1 `POST /api/v1/boards/{board_id}/invites`
**Кто:** Админ доски  
пригласить участника

**Body:**
```json
{
  "username": "username",
  "role": "member"
}
```

**Ответ:**
```json
{
  "message": "Пользователь приглашен",
  "invite": {
    "id": "uuid",
    "board_id": "uuid",
    "username": "username",
    "role": "member",
    "status": "pending"
  }
}
```

---

### 5.2 `GET /api/v1/boards/{board_id}/members`
**Кто:** Админ доски  
получить список участников

**Ответ:**
```json
{
  "items": [
    {
      "id": "uuid",
      "username": "username",
      "name": "Name",
      "photo_url": "photo.png",
      "role": "admin"
    }
  ]
}
```
