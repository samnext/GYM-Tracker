from fastapi import FastAPI, status, HTTPException
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

exercises: list[ExerciseSchema] = []





app = FastAPI()

@app.get('/exercises')
def get_available_exercises():
    return {'total': len(exercises), 'items': exercises}

@app.post('/exercises', status_code = status.HTTP_201_CREATED)
def add_exercises(payload: ExerciseCreateSchema):
    new_exercise = ExerciseSchema(
        id = len(exercises),
        name = payload.name,
        description = payload.description,
        category = payload.category,
        muscle_group = payload.muscle_group)

    exercises.append(new_exercise)
    return new_exercise

@app.get('/exercises/{id}')
def get_exercise_by_id(id: int):
    for exercise in exercises:
        if exercise.id == id:
            return exercise
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
