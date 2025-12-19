from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.core.database import get_db
from backend.models.user import User
from backend.models.schemas import RegisterAdminRequest
from backend.core.security import require_role

router = APIRouter(
    prefix="/auth-admin",
    tags=["Auth-Admin"]
)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post(
    "/register",
    dependencies=[Depends(require_role("admin"))]
)
def register(data: RegisterAdminRequest, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(
            status_code=400,
            detail="Usuário já existe"
        )
        
    if (data.role not in ["admin", "moderator", "user"]):
        raise HTTPException(
            status_code=400,
            detail="Função inválida"
        )

    user = User(
        username=data.username,
        hashed_password=pwd_context.hash(data.password),
        role=data.role,
        must_change_password=True
    )

    try:
        db.add(user)
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(500, "Erro ao criar usuário")

    return {"status": "usuário criado"}

if __name__ == '__main__':
    pass