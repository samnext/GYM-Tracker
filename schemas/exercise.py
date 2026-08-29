from pydantic import BaseModel

class ExerciseSchema(BaseModel):
    id: int
    name: str
    description: str
    category: str
    muscle_group: str
 
class ExerciseCreateSchema(BaseModel):
    name: str
    description: str
    category: str
    muscle_group: str