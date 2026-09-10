from sqlalchemy.orm import Session, selectinload
from sqlalchemy import select

from app.models.base import WorkoutORM, WorkoutItemORM


class WorkoutRepository():

    def __init__(self, db: Session):
        self.db = db

    def get_all(self):
        statement = select(WorkoutORM).options(selectinload(WorkoutORM.items))
        return list(self.db.scalars(statement).all())

    def get_by_id(self, id: int):
        statement = select(WorkoutORM).options(selectinload(WorkoutORM.items)).where(WorkoutORM.id == id)
        return self.db.scalar(statement)
    
    def create(
            self,
            title: str,
            scheduled_at: str,
            notes: str,
            status: str
            ):
        new_workout = WorkoutORM(
            title=title,
            scheduled_at=scheduled_at,
            notes=notes,
            status=status
        )

        self.db.add(new_workout)
        self.db.flush()
        return new_workout

    def save_items(self, items: list[WorkoutItemORM]):
        self.db.add_all(items)
        self.db.flush()


    def delete(self, workout: WorkoutORM):
        self.db.delete(workout)

    
        