from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    Date,
    ForeignKey
)

from backend.core.database import Base

class AlunoMateria(Base):
    __tablename__ = "aluno_materia"

    aluno_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    materia_codigo = Column(String(50), primary_key=True)
    concluida = Column(Boolean, nullable=False, default=False)
    data_conclusao = Column(Date, nullable=True)