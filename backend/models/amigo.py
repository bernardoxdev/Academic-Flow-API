import enum

from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    Enum,
    UniqueConstraint,
    CheckConstraint
)

from backend.core.database import Base

class StatusAmizade(enum.Enum):
    pendente = "pendente"
    aceita = "aceita"
    bloqueada = "bloqueada"

class Amizade(Base):
    __tablename__ = "amizades"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    amigo_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    status = Column(Enum(StatusAmizade), default=StatusAmizade.pendente, index=True, nullable=False)

    __table_args__ = (
        CheckConstraint("user_id < amigo_id", name="chk_user_amigo_order"),
        UniqueConstraint("user_id", "amigo_id", name="uq_user_amigo")
    )