from sqlalchemy.orm import Session

from app.repositories.workout import WorkoutRepository
from app.models.base import WorkoutItemORM
from app.schemas.workout import WorkoutSchema, WorkoutCreateSchema

from app.cache.redis import RedisCacheBackend
from app.db.config import settings

class WorkoutNotFound(Exception):
    pass

class WorkoutService():

    def __init__(self, db: Session):
        self.db = db
        self.workout_repository = WorkoutRepository(db)
        self.workouts_status = ('planned', 'done')
        self.cache = RedisCacheBackend(settings.redis_url, settings.cache_ttl_seconds)

    def get_all_workouts(self) -> dict[str, int | list[WorkoutSchema]]:
        #Check Redis
        cached_workouts = self.cache.get(settings.cache_workouts_key)
        if cached_workouts is not None:
            return {
            'total': len(cached_workouts),
            'items': cached_workouts
            }


        #Go to DB
        workouts_orm = self.workout_repository.get_all()
        workout_schemas = [
            WorkoutSchema.model_validate(workout) 
            for workout in workouts_orm
        ]

        #Add to Redis
        workouts_for_cache = [workout.model_dump() for workout in workout_schemas]
        self.cache.set(settings.cache_workouts_key, workouts_for_cache)

        return {
            'total': len(workout_schemas),
            'items': workout_schemas
        }

    def get_workout_by_id(self, id: int) -> WorkoutSchema:
        workout_orm = self.workout_repository.get_by_id(id)
        if not workout_orm:
            raise WorkoutNotFound(f"Workout with id={id} not found")

        return WorkoutSchema.model_validate(workout_orm)

    def create_workout(self, payload: WorkoutCreateSchema) -> WorkoutSchema:

        self.cache.delete(settings.cache_workouts_key)


        new_workout = self.workout_repository.create(
            title = payload.title,
            scheduled_at=payload.scheduled_at,
            notes = payload.notes,
            status = self.workouts_status[0]
        )
        
        items_orm = [
            WorkoutItemORM(
                workout_id=new_workout.id,
                **item.model_dump()
            )
            for item in payload.items
        ]

        self.workout_repository.save_items(items_orm)
        self.db.commit()

        return WorkoutSchema.model_validate(new_workout)

    def delete_workout(self, id: int) -> None:

        self.cache.delete(settings.cache_workouts_key)

        workout_to_delete = self.workout_repository.get_by_id(id)
        if workout_to_delete is None:
            raise WorkoutNotFound(f"Workout with id={id} not found")

        self.workout_repository.delete(workout_to_delete)
        self.db.commit()



    
