from fastapi import FastAPI
from .database import Base, engine, SessionLocal
from .models import Inscricao
from .rabbitmq import publish, start_consumer

Base.metadata.create_all(bind=engine)
app = FastAPI()

@app.on_event("startup")
def startup():
    start_consumer()

@app.post("/inscricoes")
def criar_inscricao(evento_id: int):
    db = SessionLocal()
    insc = Inscricao(evento_id=evento_id, status="CRIADA")
    db.add(insc)
    db.commit()

    publish({
        "tipo": "inscricao_criada",
        "inscricao_id": insc.id,
        "evento_id": evento_id
    })

    return {"id": insc.id, "status": insc.status}
