from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    ForeignKey
)

from backend.core.database import Base

class FazendoMateria(Base):
    __tablename__ = "fazendo_materias"

    id = Column(Integer, primary_key=True, autoincrement=True)
    id_materia = Column(Integer, index=True, nullable=False)
    id_aluno = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    fazendo = Column(Boolean, nullable=False)