# FastAPI JWT Authentication (SQLite)

A simple, production-style **user authentication system** built with **FastAPI**, **JWT**, and **SQLite**, featuring user registration, login (with email + password), and user info endpoints. Includes Swagger documentation and organized folder structure.

---

## 🧱 Project Structure

```
fastapi-jwt-auth-sqlite/
├── main.py
├── requirements.txt
├── db/
│   ├── __init__.py
│   └── session.py
├── models/
│   └── user.py
├── schemas/
│   └── user.py
├── endpoints/
│   └── auth.py
└── core/
    └── security.py
```

---

## ⚙️ Setup Instructions

### 1️⃣ Clone the Project

```bash
git clone 
cd 
```

### 2️⃣ Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Application

```bash
uvicorn main:app --reload
```

The server will start at: **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

## 🧩 Available Endpoints

### 🔹 Root

```
GET /
```

**Response:**

```json
{"message": "FastAPI JWT Auth — visit /docs for Swagger UI"}
```

---

### 🔹 Register User

```
POST /auth/register
```

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "strongpassword"
}
```

**Response:**

```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true
}
```

---

### 🔹 Login (Get JWT Token)

```
POST /auth/token
```

**Request Body:**

```json
{
  "email": "user@example.com",
  "password": "strongpassword"
}
```

**Response:**

```json
{
  "access_token": "<JWT_TOKEN>",
  "token_type": "bearer"
}
```

---

### 🔹 Get Current User

```
GET /auth/me
```

**Headers:**

```
Authorization: Bearer <JWT_TOKEN>
```

**Response:**

```json
{
  "id": 1,
  "email": "user@example.com",
  "is_active": true
}
```

---

## 🔒 JWT Configuration

Defined in `core/security.py`:

```python
SECRET_KEY = "CHANGE_THIS_TO_A_RANDOM_SECRET"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440  # 1 day
```

In production:

* Use a secure, random `SECRET_KEY` stored in environment variables.
* Use HTTPS and secure cookies.

---

## 🧠 Swagger Documentation

Swagger and ReDoc are automatically generated:

* Swagger UI → **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**
* ReDoc → **[http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)**

You can log in and test endpoints directly from the Swagger interface.

---

## 🧑‍💻 Developer Notes

* Default database: `SQLite` (stored as `app.db`).
* ORM: SQLAlchemy.
* Passwords are hashed using **bcrypt**.
* JWTs are created with **python-jose**.

---

## 🚀 Production Recommendations

1. Change the `SECRET_KEY` and move it to an environment variable.
2. Use **PostgreSQL** or **MySQL** instead of SQLite for deployment.
3. Enable **HTTPS** in production.
4. Consider **token refresh & revocation** for long sessions.

---

## 🧰 Tech Stack

* **FastAPI** — modern Python web framework.
* **SQLAlchemy** — ORM for database interaction.
* **Pydantic** — data validation and serialization.
* **Passlib** — password hashing.
* **Python-JOSE** — JWT creation and validation.

---

## 📚 License

MIT License © 2025 — Developed by **Loue Sauveur Christian (Chriss)**
