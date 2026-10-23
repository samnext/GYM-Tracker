# GYM-Tracker

Backend-app for managing exercises and workouts.

Project was build to learn FastAPI, SQLAlchemy, PostgreSQL, Docker, Redis, Pytest and the main concepts of building multi-layer backend-app. 

## Stack

* **Python 3.14**
* **FastAPI**
* **Pydantic**
* **SQLAlchemy 2.0**
* **PostgreSQL**
* **Redis**
* **Docker**
* **Docker Compose**
* **Uvicorn**

## Architecture

Multi-layer architecture was used in this project:

```text
                HTTP Request
                     │
                     ▼
              ┌─────────────┐
              │   Router    │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │   Service   │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │ Repository  │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │ SQLAlchemy  │
              └──────┬──────┘
                     │
                     ▼
              ┌─────────────┐
              │ PostgreSQL  │
              └─────────────┘
```


### Main Directories

| Directory       | Purpose                                     |
| --------------- | ----------------------------------------------- |
| `api/`          | HTTP API и FastAPI dependencies                 |
| `db/`           | DB conection and SQLAlchemy session             | 
| `models/`       | ORM-models                                      |
| `schemas/`      | Pydantic-schemas                                |
| `repositories/` | Working with DB                                 |
| `services/`     | Business-logic                                  |
| `main.py`       | main file                                       |

## Launch

### Docker Compose

Clone repo:

```bash
git clone https://github.com/samnext/GYM-Tracker.git
cd GYM-Tracker
```
Create '.env' file with DB settings.

Example:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=gym_tracker
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
To run:

```bash
docker compose up --build
```
After docker is up, API will be available on:

```text
http://localhost:8000
```
Interactive Swagger documentation:

```text
http://localhost:8000/docs
```

## API

### Exercises

End-points:

```text
GET    /exercises
GET    /exercises/{id}
POST   /exercises
```

### Workouts

End-points:

```text
GET    /workouts
GET    /workouts/{id}
POST   /workouts
DELETE /workouts/{id}
```


