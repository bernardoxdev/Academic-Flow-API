# 📚 Academic Flow API

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Framework-green)
![License](https://img.shields.io/badge/License-GPL--3.0-red)
![Status](https://img.shields.io/badge/Status-Active-success)

Academic Flow API is a **centralized RESTful backend** designed to support computer science students from UFSJ (Universidade Federal de São João Del Rei), providing authentication, academic data handling, and system integration.

---

## 📌 Project Overview

The **Academic Flow API** serves as the core backend for all Academic Flow projects.
It was designed following best practices in **software architecture**, **security**, and **scalability**, making it suitable for **academic systems, portfolios, and TCC projects**.

### Project Goals

- Centralize academic rules and data
- Enable secure frontend integration
- Apply clean backend architecture
- Serve as a reusable academic platform

---

## 🎓 Academic & Portfolio Context

This project can be used as:

- 📘 **Undergraduate Final Project (TCC)**
- 💼 **Professional Backend Portfolio**
- 🧪 **Educational Case Study**
- 🚀 **Scalable Academic Platform**

Concepts demonstrated:

- REST API Design
- JWT Authentication
- Database Modeling (ER)
- Secure Authentication Flow
- Modular Backend Architecture

---

## 🚀 Technologies Used

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **Pydantic**
- **JWT (Access & Refresh Token)**
- **PostgreSQL** (production)
- **SQLite** (development)
- **Docker**
- **Render**
- **Swagger / OpenAPI**

---

## 📂 Project Structure

```
Academic-Flow-API/
├── backend/
│   ├── api/
│   ├── config/
│   ├── data/
│   ├── data_store/
│   ├── ml/
│   ├── core/
│   ├── models/
│   ├── libs/
│   └── main.py
├── Dockerfile
├── requirements.txt
├── run.sh
├── pyproject.toml
├── LICENSE
├── README.md
└── SECURITY.md

```

---

## 🔐 Authentication

The API uses **JWT-based authentication**.

Required header:

```
Authorization: Bearer <access_token>
```

Security features:

- Encrypted passwords (bcrypt)
- Token-based authentication
- Refresh token mechanism
- Role-based access control

---

## 📘 API Documentation

Interactive API documentation is automatically generated.

- Swagger UI: https://academic-flow-api.onrender.com/docs

---

## 🧪 Example Request

```http
POST /auth/login
Content-Type: application/json

{
  "username": "student01",
  "password": "password123"
}
```

---

## 🐳 Docker Usage

```bash
docker build -t academic-flow-api .
docker run -p 8000:8000 academic-flow-api
```

---

## 🚀 Deployment (Render)

```bash
./run.sh
```

Environment variables:

- SECRET_KEY
- ADMIN_USERNAME
- ADMIN_PASSWORD
- ADMIN_ROLE
- ADMIN_EMAIL
- ACCESS_TOKEN_EXPIRE_MINUTES
- REFRESH_TOKEN_EXPIRE_DAYS
- DATABASE_URL

## 🛡️ Security Policy

Please refer to **SECURITY.md** for vulnerability reporting and security practices.

---

## 📜 License

This project is licensed under the **GPL-3.0 License**.

---

## 📌 Final Notes

Academic Flow API was developed with:

- Clean Architecture
- Educational purpose
- Professional backend standards
- Scalability and security in mind
