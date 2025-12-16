from fastapi import FastAPI
from .database import Base, engine
from .rabbitmq import start_consumer

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.on_event("startup")
def startup():
    start_consumer()
