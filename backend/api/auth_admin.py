from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from brutils import is_valid_email
from passlib.context import CryptContext
from backend.core.jwt import (
    create_access_token,
    create_refresh_token
)

from backend.models.refresh_token import RefreshToken
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
            status_code=status.HTTP_409_CONFLICT,
            detail="Usuário já existe"
        )
        
    if not is_valid_email(data.email):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email inválido"
        )

    user = User(
        username=data.username,
        email=data.email,
        matricula=data.matricula,
        hashed_password=pwd_context.hash(data.password),
        role="aluno",
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception:
        db.rollback()
        raise HTTPException(500, "Erro ao criar usuário")

    payload = {
        "sub": str(user.id),
        "role": user.role
    }

    access_token = create_access_token(payload)
    refresh_token = create_refresh_token({"sub": str(user.id)})

    try:
        db.add(RefreshToken(token=refresh_token, user_id=user.id))
        db.commit()
    except Exception:
        db.rollback()
        raise HTTPException(500, "Erro ao gerar tokens")

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

if __name__ == '__main__':
    pass