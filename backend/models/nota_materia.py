from sqlalchemy import Column, Integer
from backend.core.database import Base

class NotaMateria(Base):
    __tablename__ = "nota_materias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_materia = Column(Integer, index=True, nullable=False)
    id_aluno = Column(Integer, index=True, nullable=False)
    nota = Column(Integer, nullable=False)