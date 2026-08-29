from pydantic import BaseModel

class WorkoutExerciseSchema(BaseModel):
    exercise_id: int
    sets: int
    reps: int
    weight: int
    comment: str
    
class WorkoutSchema(BaseModel):
    id: int
    title: str
    scheduled_at: str
    status: str
    notes: str
    items: list[WorkoutExerciseSchema]

class WorkoutCreateSchema(BaseModel):
    title: str
    scheduled_at: str
    notes: str
    items: list[WorkoutExerciseSchema]


class WorkoutUpdateSchema(BaseModel):
    title: str | None = None
    scheduled_at: str | None = None
    status: str | None = None
    notes: str | None = None
    items: list[WorkoutExerciseSchema] | None = None