from collections.abc import Callable
from unittest.mock import Mock

import pytest
from app.models.base import ExerciseORM
from app.schemas.exercise import ExerciseCreateSchema, ExerciseSchema
from app.services.exercise import ExerciseNotFound, ExerciseService
from sqlalchemy.exc import SQLAlchemyError


class TestGetExerciseById:
    def test_raises_exception(
        self, exercise_service: ExerciseService, exercise_repository: Mock
    ):

        exercise_repository.get_by_id.return_value = None

        with pytest.raises(ExerciseNotFound):
            exercise_service.get_exercise_by_id(1)

        exercise_repository.get_by_id.assert_called_once_with(1)

    def test_returns_schema_when_found(
        self,
        exercise_service: ExerciseService,
        exercise_repository: Mock,
        make_exercise: Callable,
    ):

        exercise_data = make_exercise(id=0)

        exercise_orm = ExerciseORM(**exercise_data)

        exercise_repository.get_by_id.return_value = exercise_orm
        response_service = exercise_service.get_exercise_by_id(exercise_data["id"])

        assert response_service.model_dump() == exercise_data

        exercise_repository.get_by_id.assert_called_once_with(exercise_data["id"])


class TestGetAllExercises:
    def test_returns_empty_list(
        self, exercise_service: ExerciseService, exercise_repository: Mock
    ):

        # Arrange
        exercise_repository.get_all.return_value = []

        # Act
        response_service = exercise_service.get_all_exercises()

        # Assert
        assert response_service["total"] == 0
        assert response_service["items"] == []

        exercise_repository.get_all.assert_called_once_with()

    def test_returns_full_list(
        self,
        exercise_service: ExerciseService,
        exercise_repository: Mock,
        make_exercise: Callable,
    ):

        exercise_data_1 = make_exercise(
            id=1,
            name="bench press",
            description="do bench press",
            category="press",
            muscle_group="chest",
        )

        exercise_data_2 = make_exercise(
            id=2,
            name="triceps extension",
            description="do triceps extension",
            category="extension",
            muscle_group="triceps",
        )

        exercise_data_tuple = (exercise_data_1, exercise_data_2)

        exercise_orms = [
            ExerciseORM(**exercise_data) for exercise_data in exercise_data_tuple
        ]

        exercise_repository.get_all.return_value = exercise_orms

        response_service = exercise_service.get_all_exercises()

        assert response_service["total"] == 2
        assert response_service["items"] == [
            ExerciseSchema(**exercise_data) for exercise_data in exercise_data_tuple
        ]

        exercise_repository.get_all.assert_called_once_with()


class TestCreateExercise:
    def test_returns_exercise_and_commits(
        self,
        exercise_service: ExerciseService,
        exercise_repository: Mock,
        db_session: Mock,
        valid_exercise_to_create: dict[str, str],
    ):

        exercise_to_add = ExerciseCreateSchema(**valid_exercise_to_create)
        created_exercise_data = {"id": 1} | valid_exercise_to_create

        exercise_repository.create.return_value = ExerciseORM(**created_exercise_data)

        response_service = exercise_service.create_exercise(exercise_to_add)

        assert response_service.model_dump() == created_exercise_data

        exercise_repository.create.assert_called_once_with(**valid_exercise_to_create)
        db_session.commit.assert_called_once_with()

    def test_doesnt_commit_when_exception_raises(
        self,
        exercise_service: ExerciseService,
        exercise_repository: Mock,
        db_session: Mock,
        valid_exercise_to_create: dict[str, str],
    ):

        exercise_to_add = ExerciseCreateSchema(**valid_exercise_to_create)
        exercise_repository.create.side_effect = SQLAlchemyError()

        with pytest.raises(SQLAlchemyError):
            exercise_service.create_exercise(exercise_to_add)

        db_session.commit.assert_not_called()
