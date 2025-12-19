import dotenv

from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.core.database import SessionLocal
from backend.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

dotenv.load_dotenv()

ADMIN_USERNAME = dotenv.get_key(".env", "ADMIN_USERNAME")
ADMIN_PASSWORD = dotenv.get_key(".env", "ADMIN_PASSWORD")
ADMIN_ROLE = dotenv.get_key(".env", "ADMIN_ROLE")

def criar_admin_se_nao_existir():
    db: Session = SessionLocal()

    admin = db.query(User).filter(User.username == ADMIN_USERNAME).first()

    if not admin:
        admin = User(
            username=ADMIN_USERNAME,
            hashed_password=pwd_context.hash(ADMIN_PASSWORD),
            role=ADMIN_ROLE,
            must_change_password=False
        )
        db.add(admin)
        db.commit()
        print("✅ Usuário admin criado")
    else:
        print("ℹ️ Usuário admin já existe")

    db.close()