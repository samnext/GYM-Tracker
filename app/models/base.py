from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column

class Base(DeclarativeBase):
    pass

class ExerciseORM(Base):
    __tablename__ = "exercises"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    category: Mapped[str]
    muscle_group: Mapped[str]

    workout_items: Mapped[list["WorkoutItemORM"]] = relationship(back_populates="exercise")


class WorkoutORM(Base):
    __tablename__ = "workouts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(unique=True)
    scheduled_at: Mapped[str]
    status: Mapped[str]
    notes: Mapped[str]

    items: Mapped[list["WorkoutItemORM"]] = relationship(back_populates="parent_workout", cascade="all, delete")

class WorkoutItemORM(Base):
    __tablename__ = "workouts_items"

    workout_id: Mapped[int] = mapped_column(ForeignKey("workouts.id"), primary_key=True)
    exercise_id: Mapped[int] = mapped_column(ForeignKey("exercises.id"), primary_key=True)
    sets: Mapped[int]
    reps: Mapped[int]
    weight: Mapped[float]
    comment: Mapped[str]

    parent_workout: Mapped["WorkoutORM"] = relationship(back_populates="items")
    exercise: Mapped["ExerciseORM"] = relationship(back_populates="workout_items")




