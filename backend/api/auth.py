from fastapi import APIRouter, HTTPException, Depends, status
from jose import jwt, JWTError
from brutils import is_valid_email
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from backend.core.database import get_db
from backend.core.jwt import (
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM
)
from backend.core.security import get_current_user
from backend.models.user import User
from backend.models.refresh_token import RefreshToken
from backend.models.schemas import (
    LoginRequest,
    RegisterRequest,
    ChangePasswordRequest
)

router = APIRouter(prefix="/auth", tags=["Auth"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login", status_code=status.HTTP_201_CREATED)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == data.username).first()

    if not user or not pwd_context.verify(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas"
        )

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

@router.post("/refresh")
def refresh(refresh_token: str, db: Session = Depends(get_db)):
    token_db = (
        db.query(RefreshToken)
        .filter(RefreshToken.token == refresh_token)
        .first()
    )

    if not token_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token inválido"
        )

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
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(401, "Usuário não encontrado")

    new_access_token = create_access_token({
        "sub": str(user.id),
        "role": user.role
    })

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):
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
    
@router.post("/change-password")
def change_password(
    data: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == current_user.id).first()

    user.hashed_password = pwd_context.hash(data.new_password)

    db.commit()

    return {"status": "senha atualizada"}

if __name__ == '__main__':
    pass