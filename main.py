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
    title: str | None
    scheduled_at: str | None
    status: str | None
    notes: str | None
    items: list[WorkoutExerciseSchema] | None

exercises: list[ExerciseSchema] = []

workouts: list[WorkoutSchema] = []

workouts_status = ('planned', 'done')
tags = (['exercises'], ['workouts'])


app = FastAPI()

@app.get('/exercises', tags=tags[0])
def get_exercises_list():
    return {'total': len(exercises), 'items': exercises}

@app.post('/exercises', 
          status_code = status.HTTP_201_CREATED,
          tags=tags[0]
)
def add_exercise(payload: ExerciseCreateSchema):
    new_exercise = ExerciseSchema(
        id = len(exercises),
        name = payload.name,
        description = payload.description,
        category = payload.category,
        muscle_group = payload.muscle_group)

    exercises.append(new_exercise)
    return new_exercise

@app.get('/exercises/{id}', tags= tags[0])
def get_exercise_by_id(id: int):
    for exercise in exercises:
        if exercise.id == id:
            return exercise
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.get('/workouts', tags=tags[1])
def get_workouts_list():
    return {'total': len(workouts), 'items': workouts}

@app.post('/workouts', 
          status_code=status.HTTP_201_CREATED,
          tags=tags[1]
)
def create_workout(payload: WorkoutCreateSchema):
    new_workout = WorkoutSchema(
        title=payload.title,
        scheduled_at=payload.scheduled_at,
        notes=payload.notes,
        items=payload.items,
        id = len(workouts),
        status = workouts_status[0]
    )
    workouts.append(new_workout)
    return new_workout

@app.patch('/workouts/{id}', tags=tags[1])
def update_workout(id: int, payload: WorkoutUpdateSchema):
    for workout in workouts:
        if workout.id == id:

            if payload.title is not None:
                workout.title = payload.title
            if payload.scheduled_at is not None:
                workout.scheduled_at = payload.scheduled_at
            if payload.status is not None:
                workout.status = payload.status
            if payload.notes is not None:
                workout.notes = payload.notes
            if payload.items is not None:
                workout.items = payload.items
            return workout 
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)


@app.get('/workouts/{id}', tags=tags[1])
def get_workout_by_id(id: int):
    for workout in workouts:
        if workout.id == id:
            return workout
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.delete('/workouts/{id}', status_code=status.HTTP_204_NO_CONTENT,  tags=tags[1])
def delete_workout(id: int):
    for workout in workouts:
        if workout.id == id:
            workouts.remove(workout)
            return workout
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
