# OptiSlot — Priority-Based Elective Allocation System

A production-ready Django web app that allocates electives to students using a ranked-choice algorithm based on CGPA and registration timestamp.

## Features

- Student registration & login (Django auth)
- Submit top 3 ranked elective choices
- Deterministic allotment algorithm (CGPA desc → timestamp asc)
- Concurrency-safe with `select_for_update()` inside atomic transactions
- Live seat counter via AJAX polling (updates every 5s)
- Admin dashboard: run allotment, view results, export CSV
- REST API endpoints (DRF)
- Deployment-ready for Render with PostgreSQL

## Tech Stack

- Backend: Django 4.2 + Django REST Framework
- Database: PostgreSQL (SQLite for local dev)
- Frontend: Django Templates + Bootstrap 5
- Deployment: Render + Gunicorn + WhiteNoise

## Project Structure

```
optislot/
├── optislot/          # Django project config
├── users/             # Custom Student model, auth views
├── electives/         # Elective & Choice models, views, API
├── allotment/         # Allotment model, algorithm, admin views
├── templates/         # All HTML templates
├── static/            # Static assets
├── manage.py
├── requirements.txt
├── render.yaml
└── .env.example
```

## Local Setup

### 1. Clone & install dependencies

```bash
cd optislot
pip install -r requirements.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — set SECRET_KEY, DATABASE_URL (or leave default for SQLite)
```

### 3. Run migrations & seed data

```bash
python manage.py migrate
python manage.py seed_electives        # loads 8 sample electives
python manage.py createsuperuser       # create admin account
```

### 4. Start the server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/electives/` | List all electives with seat counts |
| GET | `/api/choices/` | Current user's choices |
| POST | `/api/allotment/run/` | Run allotment (admin only) |
| GET | `/api/allotment/results/` | All allotment results |

## PostgreSQL Setup

```bash
# Create DB
createdb optislot_db

# Set in .env
DATABASE_URL=postgres://youruser:yourpassword@localhost:5432/optislot_db
```

## Deployment (Render)

1. Push to GitHub
2. Create a new Web Service on [render.com](https://render.com)
3. Connect your repo — Render auto-detects `render.yaml`
4. Set `SECRET_KEY` env var in Render dashboard
5. Deploy

Live URL: _[your-render-url-here]_

## Algorithm

```
Sort students: CGPA (desc) → date_joined (asc)
For each student:
  Try Choice 1 → if seats > 0: allocate, break
  Try Choice 2 → if seats > 0: allocate, break
  Try Choice 3 → if seats > 0: allocate, break
  Else: unallotted
All within a single DB transaction with select_for_update()
```
