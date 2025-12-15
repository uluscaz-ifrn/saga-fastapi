from fastapi import FastAPI
from .rabbitmq import start_consumer

app = FastAPI()

@app.on_event("startup")
def startup():
    start_consumer()
