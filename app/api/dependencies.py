from fastapi import Depends
from sqlalchemy.orm import Session

from app.services.exercise import ExerciseService
from app.services.workout import WorkoutService
from app.db.session import get_db


def get_exercise_service(db: Session = Depends(get_db)):
    return ExerciseService(db)

def get_workout_service(db: Session = Depends(get_db)):
    return WorkoutService(db)