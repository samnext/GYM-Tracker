from sqlalchemy.orm import Session

from app.repositories.exercise import ExerciseRepository
from app.schemas.exercise import ExerciseSchema, ExerciseCreateSchema

#Redis
from app.cache.redis import RedisCacheBackend
from app.db.config import settings



class ExerciseNotFound(Exception):
    """Exercise not found in DB"""


class ExerciseService():
    def __init__(self, db: Session):
        self.db = db
        self.exercise_repository = ExerciseRepository(db)
        self.cache = RedisCacheBackend(settings.redis_url, settings.cache_ttl_seconds)


    def get_all_exercises(self) -> dict[str, int | list[ExerciseSchema]]:

        #1. Проверить Redis
        cached_exercises = self.cache.get(settings.cache_exercises_key)
        if cached_exercises is not None:
            return {
            'total': len(cached_exercises),
            'items': cached_exercises
            }

        #2. Если там нет, идем в БД
        exercises_read = self.exercise_repository.get_all()
        exercises_schemas = [
            ExerciseSchema.model_validate(exercise_orm) for exercise_orm in exercises_read
        ]
        
        #3. Добавить в Redis
        exercises_for_cache = [exercise.model_dump() for exercise in exercises_schemas]
        self.cache.set(settings.cache_exercises_key, exercises_for_cache)
        
        return {
            'total': len(exercises_schemas),
            'items': exercises_schemas
        }

    def create_exercise(self, exercise_to_create: ExerciseCreateSchema) -> ExerciseSchema:
        #1. Инвалидация кэша (очищаем кэш)
        self.cache.delete(settings.cache_exercises_key)

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
