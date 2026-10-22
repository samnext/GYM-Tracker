from typing import Annotated

from app.api.dependencies import get_exercise_service
from app.schemas.exercise import ExerciseCreateSchema, ExerciseSchema
from app.services.exercise import ExerciseNotFound, ExerciseService
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/exercises")


@router.get("")
def get_all_exercises(
    exercise_service: Annotated[ExerciseService, Depends(get_exercise_service)],
) -> dict[str, int | list[ExerciseSchema]]:
    return exercise_service.get_all_exercises()


@router.post("", status_code=status.HTTP_201_CREATED)
def create_exercise(
    payload: ExerciseCreateSchema,
    exercise_service: Annotated[ExerciseService, Depends(get_exercise_service)],
) -> ExerciseSchema:
    return exercise_service.create_exercise(exercise_to_create=payload)


@router.get("/{exercise_id}")
def get_exercise_by_id(
    exercise_id: str, exercise_service: Annotated[ExerciseService, Depends(get_exercise_service)]
) -> ExerciseSchema:
    try:
        return exercise_service.get_exercise_by_id(exercise_id=exercise_id)
    except ExerciseNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
