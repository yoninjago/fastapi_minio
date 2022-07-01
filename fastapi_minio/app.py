from fastapi import FastAPI

from .api import router
from .database.database import engine
from .database.models import Base

app = FastAPI()
app.include_router(router)

Base.metadata.create_all(bind=engine)
