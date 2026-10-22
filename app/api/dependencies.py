from typing import Annotated

from app.db.session import get_db
from app.services.exercise import ExerciseService
from app.services.workout import WorkoutService
from fastapi import Depends
from sqlalchemy.orm import Session


def get_exercise_service(db: Annotated[Session, Depends(get_db)]):
    return ExerciseService(db)


def get_workout_service(db: Annotated[Session,Depends(get_db)]):
    return WorkoutService(db)
