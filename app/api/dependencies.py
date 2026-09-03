from fastapi import Depends
from sqlalchemy.orm import Session

from app.services.exercise import ExerciseService
from app.db.session import get_db


def get_exercise_service(db: Session = Depends(get_db)):
    return ExerciseService(db)

