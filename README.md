# ONLINE POLLING SYSTEM

A simple polling system built with Django that allows users to:

- Create polls with multiple questions
- Add options to each question
- Vote on options (one vote per question per user)
- View poll results

Authentication is required — each user can vote only once per question.

---

## 🚀 Features

- User registration and login (email as username)
- JWT-based authentication (using djangorestframework-simplejwt)
- Create polls with multiple questions and options
- Prevent duplicate voting
- View results per question/option
- Admin management via Django Admin Panel

---

## 🛠️ Tech Stack

- **Backend Framework**: Django & Django REST Framework
- **Auth**: Custom `User` model with JWT Authentication
- **Database**: SQLite (for dev) / PostgreSQL (for production-ready deployment)
- **UUIDs**: Used as primary keys for all models

---

## 📁 Project Structure

This project uses a **single Django app** called `polls` to encapsulate all functionality:

```
polling_project/
├── manage.py
├── polling_project/
│   ├── settings.py
│   ├── urls.py
│   └── ...
└── polls/
    ├── models.py
    ├── serializers.py
    ├── views.py
    ├── urls.py
    └── ...
```

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/Emmanuel-Ebiwari/online-poll-system
cd polling-system
```

### 2. Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (optional, for admin access)

```bash
python manage.py createsuperuser
```

### 6. Run the Server

```bash
python manage.py runserver
```

---

<!-- ## 🔑 Authentication

JWT tokens are used for authentication.

- Obtain token:
  `POST /api/token/`
  with `{ "email": "your@email.com", "password": "yourpassword" }`

- Use the token in `Authorization` header:
  ```
  Authorization: Bearer <access_token>
  ```

--- -->

<!-- ## 🧪 API Endpoints (Examples)

| Endpoint          | Method | Description              |
| ----------------- | ------ | ------------------------ |
| `/api/polls/`     | GET    | List all polls           |
| `/api/polls/`     | POST   | Create a new poll (auth) |
| `/api/questions/` | POST   | Add question to a poll   |
| `/api/options/`   | POST   | Add option to a question |
| `/api/votes/`     | POST   | Cast a vote (auth)       |

--- -->

## 📝 License

MIT License — you are free to use and modify this project.

---

## 🙋🏽‍♂️ Author

Built by Emmanuel Ebiwari  
Linkedin: [[Emmanuel Ebiwari](https://www.linkedin.com/in/emmanuel-ebiwari-9898051a9)]  
GitHub: [[Emmanuel-Ebiwari](https://github.com/Emmanuel-Ebiwari)]
