from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from backend.core.database import Base

class ComentarioMateria(Base):
    __tablename__ = "comentario_materias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_materia = Column(Integer, index=True, nullable=False)
    id_aluno = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    comentario = Column(String(1000), nullable=False)