# Secure Employee Backend API

A secure backend application built using FastAPI.

## Features

- JWT Authentication
- Password hashing
- Role Based Access Control
- File upload
- File download
- File deletion
- API logging
- Input validation
- CORS
- Automated tests
- Docker support

## Technologies

- Python
- FastAPI
- SQLAlchemy
- SQLite
- JWT
- PyJWT
- Argon2
- Docker
- Pytest

## Installation

Create virtual environment:

python -m venv venv

Activate on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create environment file:

copy .env.example .env

Run application:

uvicorn app.main:app --reload

API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

GET /health

POST /register

POST /login

GET /users/me

GET /users

POST /files/upload

GET /files

GET /files/{file_id}

DELETE /files/{file_id}

## Roles

user:
- View own profile
- Upload files
- View own files
- Download own files

admin:
- All user permissions
- View all users
- View all files
- Delete files

## Testing

Run:

pytest -v

## Docker

Build:

docker compose build

Run:

docker compose up

API:

http://localhost:8000

Swagger:

http://localhost:8000/docs