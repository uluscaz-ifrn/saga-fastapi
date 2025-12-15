from fastapi import FastAPI
from .rabbitmq import start_consumer
from .database import Base, engine

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.on_event("startup")
def startup():
    start_consumer()
