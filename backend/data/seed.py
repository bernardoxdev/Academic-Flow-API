import os

from dotenv import load_dotenv
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.core.database import SessionLocal
from backend.models.user import User

try:
    load_dotenv()
except ImportError:
    pass

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_ROLE = os.getenv("ADMIN_ROLE")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

def criar_admin_se_nao_existir():
    db: Session = SessionLocal()

    admin = db.query(User).filter(User.username == ADMIN_USERNAME).first()

    if not admin:
        admin = User(
            username=ADMIN_USERNAME,
            email=ADMIN_EMAIL,
            matricula="0000000000",
            hashed_password=pwd_context.hash(ADMIN_PASSWORD),
            role=ADMIN_ROLE
        )
        db.add(admin)
        db.commit()
        print("✅ Usuário admin criado")
    else:
        print("ℹ️ Usuário admin já existe")

    db.close()