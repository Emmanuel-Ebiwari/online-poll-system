# ONLINE POLLING SYSTEM

A simple polling system built with Django that allows users to:

- Create polls with multiple questions
- Add options to each question
- Vote on one or multiple options per question, depending on the question type (single or multiple choice)
- View poll results

Authentication is required — only authenticated users can vote

---

## 🚀 Features

- User registration and login (email as username)
- JWT-based authentication (using djangorestframework-simplejwt)
- Create polls with multiple questions and options
- Prevent duplicate voting (if single choice question)
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

This project uses **two Django app** — polls for polling functionality and user for authentication and user management.

```
online_poll_system/
├── manage.py
├── online_poll_system/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── polls/
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── ...
└── user/
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

## 🔑 Authentication

This API uses **JWT tokens** for authentication, powered by `djangorestframework-simplejwt`.

### 🔐 Obtain Token

```http
POST /api/token/
```

**Payload:**

```json
{
  "email": "your@email.com",
  "password": "yourpassword"
}
```

### 🦁 Refresh Token

```http
POST /api/token/refresh/
```

**Payload:**

```json
{
  "refresh": "<your_refresh_token>"
}
```

### 📌 Use the Token

Include the access token in the `Authorization` header of authenticated requests:

```http
Authorization: Bearer <access_token>
```

---

## 🧺a API Endpoints

> **Note:** Only polls marked as public can be viewed without authentication. Private polls require authorization.

### 📌 Users

| Method | Endpoint                | Description                 | Auth Required |
| ------ | ----------------------- | --------------------------- | ------------- |
| GET    | `/api/user/`            | List all users (admin only) | ✅            |
| POST   | `/api/user/register/`   | Register user               | ❌            |
| POST   | `/api/user/login/`      | Login user                  | ❌            |
| GET    | `/api/user/<user_id>/`  | Retrieve a specific user    | ✅            |
| PUT    | `/api/polls/<user_id>/` | Update a user (owner only)  | ✅            |
| DELETE | `/api/polls/<user_id>/` | Delete a user (owner only)  | ✅            |

---

### 📌 Polls

| Method | Endpoint                      | Description                | Auth Required |
| ------ | ----------------------------- | -------------------------- | ------------- |
| GET    | `/api/polls/`                 | List all polls             | ❌            |
| POST   | `/api/polls/`                 | Create a new poll          | ✅            |
| GET    | `/api/polls/<poll_id>/`       | Retrieve a specific poll   | ❌            |
| PUT    | `/api/polls/<poll_id>/`       | Update a poll (owner only) | ✅            |
| DELETE | `/api/polls/<poll_id>/`       | Delete a poll (owner only) | ✅            |
| POST   | `/api/polls/<poll_id>/close/` | Close a poll (owner only)  | ✅            |

---

### 📌 Questions

| Method | Endpoint                                        | Description                            | Auth Required |
| ------ | ----------------------------------------------- | -------------------------------------- | ------------- |
| GET    | `/api/polls/<poll_id>/questions/`               | Retrieve all questions from a poll     | ✅            |
| POST   | `/api/polls/<poll_id>/questions/`               | Create a question for a poll           | ✅            |
| GET    | `/api/polls/<poll_id>/questions/<question_id>/` | Retrieve a single question and options | ❌            |
| PUT    | `/api/polls/<poll_id>/questions/<question_id>/` | Update a single question and options   | ❌            |
| DELETE | `/api/polls/<poll_id>/questions/<question_id>/` | delete a single question and options   | ❌            |

---

### 📌 Votes

| Method | Endpoint                                              | Description                              | Auth Required |
| ------ | ----------------------------------------------------- | ---------------------------------------- | ------------- |
| POST   | `/api/polls/<poll_id>/questions/<question_id>/votes/` | Cast a vote (one vote per question/user) | ✅            |

---

### 📌 Results

| Method | Endpoint                        | Description       | Auth Required |
| ------ | ------------------------------- | ----------------- | ------------- |
| GET    | `/api/polls/<poll_id>/results/` | View poll results | ❌            |

---

### 📌 Documentation

| Method | Endpoint     | Description              |
| ------ | ------------ | ------------------------ |
| GET    | `/api/docs/` | Swagger UI documentation |

## 📝 License

MIT License — you are free to use and modify this project.

---

## 🙋🏽‍♂️ Author

Built by Emmanuel Ebiwari  
Linkedin: [[Emmanuel Ebiwari](https://www.linkedin.com/in/emmanuel-ebiwari-9898051a9)]  
GitHub: [[Emmanuel-Ebiwari](https://github.com/Emmanuel-Ebiwari)]
