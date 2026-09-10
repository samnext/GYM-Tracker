from fastapi import APIRouter, Depends, HTTPException, status

from app.services.workout import WorkoutService, WorkoutNotFound
from app.schemas.workout import WorkoutSchema, WorkoutCreateSchema, WorkoutUpdateSchema
from app.api.dependencies import get_workout_service

router = APIRouter(prefix='/workouts')

@router.get('')
def get_all_workouts(
    workout_service: WorkoutService = Depends(get_workout_service)
) -> dict[str, int | list[WorkoutSchema]]:
    return workout_service.get_all_workouts()

@router.get('/{id}')
def get_workout_by_id(
    id: int,
    workout_service: WorkoutService = Depends(get_workout_service)
) -> WorkoutSchema:
    try:
        return workout_service.get_workout_by_id(id)
    except WorkoutNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@router.post('', status_code=status.HTTP_201_CREATED)
def create_workout(
    payload: WorkoutCreateSchema,
    workout_service: WorkoutService = Depends(get_workout_service)  
) -> WorkoutSchema:
    try:
        return workout_service.create_workout(payload)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="One of the exercises wasn't found in exercises list")


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_workout(
    id: int, 
    workout_service: WorkoutService = Depends(get_workout_service)
) -> None:
    try:
        workout_service.delete_workout(id)
    except WorkoutNotFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Workout not found")
    