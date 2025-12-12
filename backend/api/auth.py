from fastapi import APIRouter, HTTPException, Depends
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.core.database import SessionLocal
from backend.core.jwt import (
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM
)
from backend.core.security import get_current_user
from backend.models.user import User
from backend.models.refresh_token import RefreshToken
from backend.models.schemas import LoginRequest, RegisterRequest, ChangePasswordRequest

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
def login(data: LoginRequest):
    db: Session = SessionLocal()

    user = db.query(User).filter(User.username == data.username).first()

    if not user or not pwd_context.verify(data.password, user.hashed_password):
        db.close()
        raise HTTPException(status_code=401, detail="Credenciais inválidas")

    if user.must_change_password:
        db.close()
        return {
            "detail": "Troca de senha obrigatória",
            "must_change_password": True,
            "user_id": user.id
        }

    access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    refresh_token = create_refresh_token({
        "sub": str(user.id)
    })

    db.add(RefreshToken(token=refresh_token, user_id=user.id))
    db.commit()
    db.close()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh(refresh_token: str):
    db: Session = SessionLocal()

    token_db = db.query(RefreshToken).filter(
        RefreshToken.token == refresh_token
    ).first()

    if not token_db:
        db.close()
        raise HTTPException(status_code=401, detail="Refresh token inválido")

    try:
        payload = jwt.decode(
            refresh_token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401)

        user_id = payload.get("sub")

    except JWTError:
        db.close()
        raise HTTPException(status_code=401, detail="Token inválido")

    new_access_token = create_access_token({
        "sub": user_id
    })

    db.close()

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }
    
@router.post("/register")
def register(data: RegisterRequest):
    db: Session = SessionLocal()

    if db.query(User).filter(User.username == data.username).first():
        db.close()
        raise HTTPException(status_code=400, detail="Usuário já existe")

    user = User(
        username=data.username,
        hashed_password=pwd_context.hash(data.password),
        role="aluno",
        must_change_password=False
    )

    db.add(user)
    db.commit()
    db.close()

    return {"status": "usuário criado"}

@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user)
):
    db: Session = SessionLocal()

    user = db.query(User).filter(User.id == current_user.id).first()

    user.hashed_password = pwd_context.hash(data.new_password)
    user.must_change_password = False
    db.commit()
    db.close()

    return {"status": "senha atualizada"}

if __name__ == '__main__':
    pass