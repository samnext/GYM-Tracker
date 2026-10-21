import pytest
import unittest.mock
from app.services.exercise import ExerciseService

@pytest.fixture
def exercise_service():
    with unittest.mock.patch(
        'app.services.exercise.ExerciseRepository'
    ):
        yield ExerciseService(unittest.mock.Mock())