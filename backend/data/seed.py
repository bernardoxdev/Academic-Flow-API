from passlib.context import CryptContext
from sqlalchemy.orm import Session

from backend.core.database import SessionLocal, engine, Base
from backend.models.user import User
from backend.core.config import ADMIN_USERNAME, ADMIN_PASSWORD

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

def seed():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()

    admin = db.query(User).filter(User.username == ADMIN_USERNAME).first()
    
    if admin:
        print("⚠️ Admin já existe")
        db.close()
        return

    user = User(
        username=ADMIN_USERNAME,
        hashed_password=pwd.hash(ADMIN_PASSWORD),
        role="admin",
        must_change_password=True
    )

    db.add(user)
    db.commit()
    db.close()

    print("✅ Admin criado via seed")

if __name__ == "__main__":
    seed()