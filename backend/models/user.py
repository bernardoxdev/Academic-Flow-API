from sqlalchemy import Column, Integer, String, Boolean
from backend.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String)
    must_change_password = Column(Boolean, default=True)