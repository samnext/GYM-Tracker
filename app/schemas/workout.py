from pydantic import BaseModel
from pydantic.config import ConfigDict

class WorkoutItemSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    exercise_id: int
    sets: int
    reps: int
    weight: float
    comment: str
    
class WorkoutSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    scheduled_at: str
    status: str
    notes: str
    items: list[WorkoutItemSchema]

class WorkoutCreateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    scheduled_at: str
    notes: str
    items: list[WorkoutItemSchema]


class WorkoutUpdateSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    title: str | None = None
    scheduled_at: str | None = None
    status: str | None = None
    notes: str | None = None
    items: list[WorkoutItemSchema] | None = None