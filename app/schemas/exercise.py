from pydantic import BaseModel
from pydantic.config import ConfigDict

class ExerciseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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

