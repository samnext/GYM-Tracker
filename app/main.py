from fastapi import FastAPI, status, HTTPException

from schemas.exercise import ExerciseSchema, ExerciseCreateSchema
from schemas.workout import  WorkoutCreateSchema, WorkoutSchema, WorkoutUpdateSchema


exercises: list[ExerciseSchema] = []
exercises_ids = set()

workouts: list[WorkoutSchema] = []

workouts_status = ('planned', 'done')
tags = (['exercises'], ['workouts'])




app = FastAPI()

@app.get('/exercises', tags=tags[0])
def get_exercises_list() -> list[int, list[ExerciseSchema]]:
    return {'total': len(exercises), 'items': exercises}

@app.post('/exercises', 
          status_code = status.HTTP_201_CREATED,
          tags=tags[0]
)
def add_exercise(payload: ExerciseCreateSchema) -> ExerciseSchema:
    new_exercise = ExerciseSchema(
        id = len(exercises),
        name = payload.name,
        description = payload.description,
        category = payload.category,
        muscle_group = payload.muscle_group)

    exercises.append(new_exercise)
    exercises_ids.add(new_exercise.id)
    return new_exercise

@app.get('/exercises/{id}', tags= tags[0])
def get_exercise_by_id(id: int) -> ExerciseSchema:
    for exercise in exercises:
        if exercise.id == id:
            return exercise
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.get('/workouts', tags=tags[1])
def get_workouts_list() -> dict[str, list[WorkoutSchema]]:
    return {'total': len(workouts), 'items': workouts}

@app.post('/workouts', 
          status_code=status.HTTP_201_CREATED,
          tags=tags[1]
)
def create_workout(payload: WorkoutCreateSchema) -> WorkoutSchema:
    for exercise in payload.items:
        if exercise.exercise_id in exercises_ids:
            new_workout = WorkoutSchema(
                title=payload.title,
                scheduled_at=payload.scheduled_at,
                notes=payload.notes,
                items=payload.items,
                id = len(workouts),
                status = workouts_status[0]
            )
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Exercise not found')
    workouts.append(new_workout)
    return new_workout

@app.patch('/workouts/{id}', tags=tags[1])
def update_workout(id: int, payload: WorkoutUpdateSchema) -> WorkoutSchema:
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
                for exercise in payload.items:
                    if exercise.exercise_id in exercises_ids:
                        workout.items = payload.items
                    else:
                        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Exercise not found')
            return workout 
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Workout not found')


@app.get('/workouts/{id}', tags=tags[1])
def get_workout_by_id(id: int) -> WorkoutSchema:
    for workout in workouts:
        if workout.id == id:
            return workout
        
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.delete('/workouts/{id}', status_code=status.HTTP_204_NO_CONTENT,  tags=tags[1])
def delete_workout(id: int) -> WorkoutSchema:
    for workout in workouts:
        if workout.id == id:
            workouts.remove(workout)
            return workout
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
