from sqlalchemy import Column, Integer
from backend.core.database import Base

class DificuldadeMateria(Base):
    __tablename__ = "dificuldade_materias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_materia = Column(Integer, index=True, nullable=False)
    id_aluno = Column(Integer, index=True, nullable=False)
    dificuldade = Column(Integer, nullable=False)