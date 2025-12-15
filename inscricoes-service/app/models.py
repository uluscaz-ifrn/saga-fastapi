from sqlalchemy import Column, Integer, String
from .database import Base

class Inscricao(Base):
    __tablename__ = "inscricoes"
    id = Column(Integer, primary_key=True)
    evento_id = Column(Integer)
    status = Column(String, default="CRIADA")
