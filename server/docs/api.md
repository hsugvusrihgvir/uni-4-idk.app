# API  
  
## 1) Auth  
  
### 1.1 `POST /api/v1/auth/login`  
**Кто:** Гость    
Отправить email и проверить, есть ли аккаунт.
  
**Body:**  
```json  
{  
  "email": "user@example.com"
}  
```  
  
**Ответ, если аккаунт есть:**  
```json  
{  
  "exists": true,  
  "message": "Код отправлен"
}  
```  
  
**Ответ, если аккаунта нет:**  
```json  
{  
  "exists": false,  
  "message": "Аккаунт не найден"
}  
```  
  
---  
  
### 1.2 `POST /api/v1/auth/register`  
**Кто:** Гость    
Создать аккаунт и отправить код.  
  
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
  "message": "Код отправлен"
}  
```  
  
---  
  
### 1.3 `POST /api/v1/auth/verify`  
**Кто:** Гость    
Подтвердить код.  
  
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
  "token_type": "bearer",  
  "user": {    
	  "email": "user@example.com",    
	  "username": "username",    
	  "name": "User",    
	  "photo_url": "photo.png"  
  }
}  
```  
  
---  
  
### 1.4 `POST /api/v1/auth/refresh`  
**Кто:** Пользователь    
Получить новый access-токен.  
  
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
Проверить username на занятость.  
  
**Ответ, если занят:**  
```json  
{  
  "available": false,  
  "message": "Username уже занят"
}  
```  
  
**Ответ, если свободен:**  
```json  
{  
  "available": true,  
  "message": "Username доступен"
}  
```  
  
---  
  
### 2.2 `GET /api/v1/users/me`  
**Кто:** Пользователь    
Получить свой профиль.  
  
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
Изменить свой профиль.  
  
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
  

### 2.4 `POST /api/v1/users/avatar`  
**Кто:** Гость  
Загрузить аватарку пользователя. Используется перед регистрацией, чтобы получить `photo_url`.

**Body:** `multipart/form-data`  

Поле:
```text
file: image/jpeg | image/png | image/webp
```

**Ответ:**
```json
{
  "photo_url": "/uploads/avatars/avatar.jpg"
}
```

---  
## 3) Boards  
  
### 3.1 `POST /api/v1/boards`  
**Кто:** Пользователь    
Создать доску.  
  
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
Получить список моих досок.  
  
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
Получить конкретную доску, идеи и мою роль.  
  
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
  
### 3.4 `PATCH /api/v1/boards/{board_id}`  
**Кто:** Админ доски    
Изменить настройки доски.  
  
**Body:**  
```json  
{  
  "title": "New title",  
  "description": "new description",  
  "moderation": true,  
  "anon_ideas": false
}  
```  
  
**Ответ:**  
```json  
{  
  "id": "uuid",  
  "title": "New title",  
  "description": "new description",  
  "moderation": true,  
  "anon_ideas": false
}  
```  
  
---  
  
### 3.5 `DELETE /api/v1/boards/{board_id}`  
**Кто:** Админ доски    
Удалить доску.  
  
**Ответ:** `204 No Content`  
  
---  
  

### 3.6 `POST /api/v1/boards/{board_id}/join`  
**Кто:** Пользователь  
Присоединиться к доске по ссылке или QR-коду.  

QR-код на фронте хранит ссылку вида:
```text
http://localhost:5173/invite/{board_id}
```

После входа фронт вызывает эту ручку. Если пользователь уже есть на доске, повторно он не добавляется.

**Ответ:**
```json
{
  "id": "uuid",
  "title": "Board 1",
  "description": "description",
  "role": "member"
}
```

---  
## 4) Ideas  
  
### 4.1 `POST /api/v1/ideas`  
**Кто:** Пользователь доски    
Добавить идею.  
  
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
Получить список идей доски.  
  
**Ответ:**  
```json  
{  
  "items": [    
			  {      
				  "id": "uuid",      
				  "board_id": "uuid",      
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
  
### 4.3 `DELETE /api/v1/ideas/{idea_id}`  
**Кто:** Автор идеи    
Удалить свою идею.  
  
**Ответ:** `204 No Content`  
  
---  
  
### 4.4 `PATCH /api/v1/ideas/{idea_id}/status`  
**Кто:** Модератор или админ доски    
Изменить статус идеи.  
  
**Body:**  
```json  
{  
  "status": "approved",  
  "rejection_reason": null
}  
```  
  
**Ответ:**  
```json  
{  
  "id": "uuid",  
  "board_id": "uuid",  
  "title": "Idea 1",  
  "description": "description",  
  "status": "approved",  
  "is_anonymous": true,  
  "created_at": "01.01.2000"
}  
```  
  
---  
  
### 4.5 `GET /api/v1/boards/{board_id}/ideas/moderation`  
**Кто:** Модератор или админ доски    
Получить идеи, которые ждут модерации.  
  
**Ответ:**  
```json  
{  
  "items": [    
			  {      
				  "id": "uuid",      
				  "title": "Idea 1",      
				  "description": "description",  
				  "status": "pending",    
				  "is_anonymous": false,     
				  "created_at": "01.01.2000"    
			  }  
		   ]
}  
```  
  
---  
  
### 4.6 `WS /api/v1/boards/{board_id}/ideas/ws?token=access_token`  
**Кто:** Пользователь доски    
Получать идеи в реальном времени.  
  
**Сообщение при новой идее:**  
```json  
{  
  "type": "idea_created",  
  "idea": 
	  {    
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
  
## 5) Members  
  
### 5.1 `GET /api/v1/boards/{board_id}/members`  
**Кто:** Пользователь доски    
Получить участников доски.  
  
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
  
---  
  
### 5.2 `POST /api/v1/boards/{board_id}/members`  
**Кто:** Админ доски    
Добавить участника на доску.  
  
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
  "id": "uuid",  
  "username": "username",  
  "name": "Name",  
  "photo_url": "photo.png",  
  "role": "member"
}  
```  
  
---  
  
### 5.3 `PATCH /api/v1/boards/{board_id}/members/{user_id}/role`  
**Кто:** Админ доски    
Изменить роль участника.  
  
**Body:**  
```json  
{  
  "role": "moderator"
}  
```  
  
**Ответ:**  
```json  
{  
  "id": "uuid",  
  "username": "username",  
  "name": "Name",  
  "photo_url": "photo.png",  
  "role": "moderator"
}  
```  
  
---  
  
### 5.4 `DELETE /api/v1/boards/{board_id}/members/{user_id}`  
**Кто:** Админ доски    
Удалить участника с доски.  
  
**Ответ:** `204 No Content`  
  
---  
  
## 6) Votings  
  
### 6.1 `POST /api/v1/boards/{board_id}/votings`  
**Кто:** Админ доски    
Создать голосование.  
  
**Body:**  
```json  
{  
  "type": "yes_no"
}  
```  
  
**Ответ:**  
```json  
{  
  "id": "uuid",  
  "board_id": "uuid",  
  "type": "yes_no",  
  "created_at": "01.01.2000"
}  
```  
  
---  
  
### 6.2 `GET /api/v1/boards/{board_id}/votings`  
**Кто:** Пользователь доски    
Получить голосования доски.  
  
**Ответ:**  
```json  
{  
  "items": [    
	  {      
		  "id": "uuid",      
		  "board_id": "uuid",      
		  "type": "yes_no",      
		  "created_at": "01.01.2000"    
	  }  
   ]
}  
```  
  
---  
  
### 6.3 `DELETE /api/v1/votings/{voting_id}`  
**Кто:** Админ доски    
Удалить голосование.  
  
**Ответ:** `204 No Content`  
  
---  
  
## 7) Votes  
  
### 7.1 `POST /api/v1/votes`  
**Кто:** Пользователь доски    
Проголосовать за идею.  
  
**Body:**  
```json  
{  
  "voting_id": "uuid",  
  "idea_id": "uuid"
}  
```  
  
**Ответ:**  
```json  
{  
  "id": "uuid",  
  "voting_id": "uuid",  
  "idea_id": "uuid",  
  "created_at": "01.01.2000"
}  
```  
  
---  
  
### 7.2 `GET /api/v1/votings/{voting_id}/results`  
**Кто:** Пользователь доски    
Получить результаты голосования.  
  
**Ответ:**  
```json  
{  
  "items": [    
	  {      
		  "idea_id": "uuid",      
		  "title": "Idea 1",      
		  "votes_count": 10,      
		  "approval_percent": 80    
	  }  
  ]
}  
```  
  
---  
  
## 8) Notifications  
  
### 8.1 `GET /api/v1/notifications`  
**Кто:** Пользователь    
Получить мои уведомления.  
  
**Ответ:**  
```json  
{  
  "items": [    
	  {      
		  "id": "uuid",      
		  "text": "Вас добавили на доску",    
		  "board_id": "uuid",      
		  "created_at": "01.01.2000"    
	  }  
  ]
}  
```  
  
---  
  
### 8.2 `DELETE /api/v1/notifications/{notification_id}`  
**Кто:** Пользователь    
Удалить свое уведомление.  
  
**Ответ:** `204 No Content`  
  
---  
  
## 9) Export  
  
### 9.1 `GET /api/v1/boards/{board_id}/ideas/export?format=txt`  
**Кто:** Модератор или админ доски    
Экспортировать идеи.  
  
**Ответ:** файл `ideas.txt`  
  
---  
  
## 10) AI  
  
### 10.1 `POST /api/v1/boards/{board_id}/ideas/summary`  
**Кто:** Модератор или админ доски    
Получить AI-сводку по идеям.  
  
**Body:**  
```json  
{  
  "min_approval_percent": 50 
}  
```  
  
**Ответ:**  
```json  
{  
  "summary": "Краткая сводка по выбранным идеям"
}  
```
