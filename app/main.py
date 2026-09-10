from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.db.session import engine
from app.models.base import Base
from app.api.routers.exercise import router as exercise_router
from app.api.routers.workout import router as workout_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    print('Lifespan is working')
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router=exercise_router, tags=['exercises'])
app.include_router(router=workout_router, tags=['workouts'])