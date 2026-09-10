# GYM-Tracker

# GYM Tracker

Backend-приложение для управления тренировками и упражнениями.

Проект разработан как учебный проект для изучения **FastAPI, SQLAlchemy, PostgreSQL, Docker и принципов построения многослойного backend-приложения**.

Основная цель — реализовать CRUD API и разобраться в том, как строится backend-приложение и как разделять ответственность между его компонентами.

## 🛠️ Стек

* **Python 3**
* **FastAPI**
* **Pydantic**
* **SQLAlchemy 2.0**
* **PostgreSQL**
* **Docker**
* **Docker Compose**
* **Uvicorn**

## 🏗️ Архитектура

В проекте используется многослойная архитектура:

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

### Router

Отвечает за HTTP-уровень приложения:

* определяет endpoints;
* принимает запросы;
* валидирует входные данные через Pydantic;
* вызывает соответствующий service;
* возвращает HTTP-ответ.

Router не содержит бизнес-логику и напрямую не работает с базой данных.

### Service

Содержит логику приложения.

Service отвечает за:

* выполнение сценариев приложения;
* проверку существования сущностей;
* работу с несколькими repository в рамках одной операции;
* управление транзакцией;
* преобразование ORM-моделей в response schemas.

### Repository

Отвечает за взаимодействие с базой данных.

Repository инкапсулирует SQLAlchemy-запросы и операции с ORM-моделями.

## 📦 Модель данных

Основные сущности проекта:

```text
Exercise
    │
    │
    ▼
WorkoutItem
    ▲
    │
    │
Workout
```

`Workout` и `Exercise` связаны отношением **many-to-many** через `WorkoutItem`.

Это необходимо, поскольку связь между тренировкой и упражнением имеет собственные данные, например:

* количество подходов;
* количество повторений;
* вес.

Поэтому `WorkoutItem` выступает в роли association object.

Упрощённо модель выглядит следующим образом:

```text
Workout
 ├── id
 ├── title
 ├── scheduled_at
 ├── status
 └── items
       │
       ├── exercise
       ├── sets
       ├── reps
       └── weight


Exercise
 ├── id
 ├── name
 └── ...
```

## 📁 Структура проекта

```text
app/
├── api/
│   ├── dependencies.py
│   └── routers/
│
├── db/
│   ├── config.py
│   └── session.py
│
├── models/
│
├── repositories/
│   ├── exercise.py
│   └── workout.py
│
├── schemas/
│
├── services/
│   ├── exercise.py
│   └── workout.py
│
└── main.py

Dockerfile
docker-compose.yml
requirements.txt
```

### Основные директории

| Директория      | Назначение                                      |
| --------------- | ----------------------------------------------- |
| `api/`          | HTTP API и FastAPI dependencies                 |
| `db/`           | Настройка подключения к БД и SQLAlchemy session |
| `models/`       | ORM-модели                                      |
| `schemas/`      | Pydantic-схемы                                  |
| `repositories/` | Работа с БД                                     |
| `services/`     | Бизнес-логика                                   |
| `main.py`       | Точка входа приложения                          |

## 🚀 Запуск

### С помощью Docker Compose

Клонировать репозиторий:

```bash
git clone https://github.com/samnext/GYM-Tracker.git
cd GYM-Tracker
```

Создать файл `.env` с настройками базы данных.

Пример:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=gym_tracker
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

Запустить приложение:

```bash
docker compose up --build
```

После запуска API будет доступно по адресу:

```text
http://localhost:8000
```

Интерактивная документация FastAPI:

```text
http://localhost:8000/docs
```

Также доступна альтернативная документация:

```text
http://localhost:8000/redoc
```

## 🔌 API

### Exercises

Основные операции:

```text
GET    /exercises
GET    /exercises/{id}
POST   /exercises
```

### Workouts

Основные операции:

```text
GET    /workouts
GET    /workouts/{id}
POST   /workouts
DELETE /workouts/{id}
```

Актуальный список endpoints и их параметры доступен в Swagger:

```text
http://localhost:8000/docs
```

## ❗Дисклеймер

Этот проект создавался прежде всего как практическая работа с backend-разработкой.

Были изучены многие аспект разработки приложения.
Отдельное внимание уделялось работе с отношениями `one-to-many` и `many-to-many`, транзакциями и разделением ответственности между слоями приложения.

