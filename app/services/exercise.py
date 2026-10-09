from sqlalchemy.orm import Session

from app.repositories.exercise import ExerciseRepository
from app.schemas.exercise import *

class ExerciseNotFound(Exception):
    """Exercise not found in DB"""


class ExerciseService():
    def __init__(self, db: Session):
        self.db = db
        self.exercise_repository = ExerciseRepository(db)


    def get_all_exercises(self) -> dict[str, int | list[ExerciseSchema]]:
        exercises_schemas = [
            ExerciseSchema.model_validate(exercise_orm) for exercise_orm in self.exercise_repository.get_all()
        ]
        return {
            'total': len(exercises_schemas),
            'items': exercises_schemas
        }

    def create_exercise(self, exercise_to_create: ExerciseCreateSchema) -> ExerciseSchema:
        new_exercise = self.exercise_repository.create(
            name=exercise_to_create.name,
            description=exercise_to_create.description,
            category=exercise_to_create.category,
            muscle_group=exercise_to_create.muscle_group
        )
        self.db.commit()

        return ExerciseSchema.model_validate(new_exercise)

    def get_exercise_by_id(self, exercise_id: int) -> ExerciseSchema:
        exercise = self.exercise_repository.get_by_id(exercise_id)
        if exercise is not None:
            return ExerciseSchema.model_validate(exercise)
        else:
            raise ExerciseNotFound(f"Exercises with id={exercise_id} not found")
