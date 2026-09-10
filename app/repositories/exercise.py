from sqlalchemy.orm import Session
from sqlalchemy import select

from app.models.base import *

class ExerciseRepository():
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[ExerciseORM]:
        exercises_orm = [
            exercise for exercise in self.db.scalars(select(ExerciseORM)).all()
        ]
        return exercises_orm

    def create(
        self, 
        name: str, 
        description: str, 
        category: str, 
        muscle_group: str
    ) -> ExerciseORM:

        new_exercise = ExerciseORM(
            name = name,
            description = description,
            category = category,
            muscle_group = muscle_group
        )
        self.db.add(new_exercise)
        return new_exercise

    def get_by_id(self, id: str) -> ExerciseORM:

        exercise_orm = self.db.get(ExerciseORM, id)
        return exercise_orm

    
