from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager

from app.schemas.workout import *
from app.schemas.exercise import *
from app.db.session import get_db, engine

from app.models.base import *

from app.api.routers.exercise import router as exercise_router



workouts_status = ('planned', 'done')
tags = (['exercises'], ['workouts'])


@asynccontextmanager
async def lifespan(_: FastAPI):
    print('Lifespan is working')
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router=exercise_router, tags=['exercises'])




def workout_item_to_schema(workout_item: WorkoutItemORM) -> WorkoutItemSchema:
    workout_item_schema = WorkoutItemSchema(
        exercise_id=workout_item.exercise_id,
        sets=workout_item.sets,
        reps=workout_item.reps,
        weight=workout_item.reps,
        comment=workout_item.comment
    )
    return workout_item_schema

def workout_orm_to_schema(workout_orm: WorkoutORM) -> WorkoutSchema:
    return WorkoutSchema(
        id=workout_orm.id,
        title=workout_orm.title,
        scheduled_at=workout_orm.scheduled_at,
        status=workout_orm.status,
        notes=workout_orm.notes,
        items=[workout_item_to_schema(x) for x in workout_orm.workout]
    )



#Workouts


@app.get('/workouts', tags=tags[1])
def get_workouts_list(db: Session = Depends(get_db)) -> dict[str, int | list[WorkoutSchema]]:
    workout_schemas = [
        workout_orm_to_schema(workout) for workout in db.scalars(select(WorkoutORM)).all()
    ]
    return {
        'total': len(workout_schemas),
        'items': workout_schemas
    }
    

@app.post('/workouts', 
          status_code=status.HTTP_201_CREATED,
          tags=tags[1]
)
def create_workout(payload: WorkoutCreateSchema, db: Session = Depends(get_db)) -> WorkoutSchema:
    new_workout = WorkoutORM(
        title = payload.title,
        scheduled_at = payload.scheduled_at,
        notes = payload.notes,
        status = workouts_status[0]
    )
    db.add(new_workout)
    db.flush()

    workout_items_to_add = [
        WorkoutItemORM(
            workout_id = new_workout.id,
            exercise_id = workout_item.exercise_id,
            sets = workout_item.sets,
            reps = workout_item.reps,
            weight = workout_item.weight,
            comment = workout_item.comment
        ) 
        for workout_item in payload.items
        ]
    db.flush()
    db.add_all(workout_items_to_add)
    db.commit()

    return workout_orm_to_schema(new_workout)
    

@app.patch('/workouts/{id}', tags=tags[1])
def update_workout(id: int, payload: WorkoutUpdateSchema, db: Session = Depends(get_db)) -> WorkoutSchema:
    workout_for_update = db.get(WorkoutORM, id)

    if workout_for_update is not None:
        if payload.title is not None:
            workout_for_update.title = payload.title
        if payload.status is not None and payload.status in workouts_status:
            workout_for_update.status = payload.status
        if payload.notes is not None:
            workout_for_update.notes = payload.notes
        if payload.scheduled_at is not None:
            workout_for_update.scheduled_at = payload.scheduled_at
        if payload.items is not None:
            
            workout_items_to_update = [
                WorkoutItemORM(
                workout_id = workout_for_update.id,
                exercise_id = workout_item.exercise_id,
                sets = workout_item.sets,
                reps = workout_item.reps,
                weight = workout_item.weight,
                comment = workout_item.comment 
                ) 
                for workout_item in payload.items
            ]
            for workout_delete in workout_for_update.workout:
                db.delete(workout_delete)
            db.flush()
            db.add_all(workout_items_to_update)
            
        db.commit()    
    else:   
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Workout not found')
    return workout_orm_to_schema(workout_for_update)


@app.get('/workouts/{id}', tags=tags[1])
def get_workout_by_id(id: int, db: Session = Depends(get_db)) -> WorkoutSchema:
    workout_orm = db.get(WorkoutORM, id)

    if workout_orm is not None:
        return workout_orm_to_schema(workout_orm)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.delete('/workouts/{id}', status_code=status.HTTP_204_NO_CONTENT,  tags=tags[1])
def delete_workout(id: int, db: Session = Depends(get_db)) -> None:
    workout_orm_for_delete = db.get(WorkoutORM, id)

    if workout_orm_to_schema is not None:
        db.delete(workout_orm_for_delete)
        db.commit()
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
