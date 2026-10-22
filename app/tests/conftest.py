from unittest.mock import Mock, patch

import pytest
from app.services.exercise import ExerciseService


@pytest.fixture
def db_session():
    return Mock()


@pytest.fixture
def exercise_service(db_session: Mock):
    with patch("app.services.exercise.ExerciseRepository"):
        yield ExerciseService(db_session)


@pytest.fixture
def valid_exercise_to_create():
    return {
        "name": "bench press",
        "description": "do bench press",
        "category": "press",
        "muscle_group": "chest",
    }


@pytest.fixture
def exercise_repository(exercise_service):
    return exercise_service.exercise_repository


@pytest.fixture
def make_exercise():
    def make(
        id=99999,
        name="def_name",
        description="def_description",
        category="def_category",
        muscle_group="def_muscle_group",
    ):
        return {
            "id": id,
            "name": name,
            "description": description,
            "category": category,
            "muscle_group": muscle_group,
        }

    return make
