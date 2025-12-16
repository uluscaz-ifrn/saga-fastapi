from sqlalchemy import Column, Integer
from .database import Base

class Vaga(Base):
    __tablename__ = "vagas"
    evento_id = Column(Integer, primary_key=True)
    total = Column(Integer)
    ocupadas = Column(Integer, default=0)
