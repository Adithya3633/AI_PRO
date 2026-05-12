# AI-Powered Interview Preparation Platform

A beginner-friendly Django full-stack project for technical interview practice.

## Stack

- Frontend: HTML, CSS, Tailwind CSS CDN, JavaScript, DOM manipulation
- Backend: Python, Django
- Database: MySQL-ready settings with SQLite fallback for quick demos
- AI: Gemini API from Django views/services
- Reports: ReportLab PDF generation

## Features

- Landing page with responsive sections
- Registration, login, logout, session-based auth
- Dashboard with total interviews, average score, best score, accuracy, recent activity
- Role selection and interview type selection
- MCQ module with timer, progress bar, random questions, local storage, instant scoring
- Subjective module with Gemini question generation and evaluation
- Coding challenge placeholder that saves submitted code
- Role-wise leaderboard
- Downloadable PDF performance report
- Django admin for users, roles, questions, scores, attempts, and leaderboard

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000`.

## MySQL

Set these values in `.env`:

```env
DB_ENGINE=mysql
DB_NAME=interview_prep
DB_USER=root
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=3306
```

Create the database in MySQL before running migrations.

## Gemini

Set `GEMINI_API_KEY` in `.env`. Without a key, the subjective module uses demo fallback text so the flow still works during presentations.
