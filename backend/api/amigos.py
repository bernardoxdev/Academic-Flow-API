from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.security import get_current_user
from backend.core.amigo_core import AmigoCore
from backend.models.user import User
from backend.models.schemas import (
    AmizadeCreate,
    AmizadeResponse,
    AmigoResponse
)

router = APIRouter(prefix="/amigos", tags=["Amizades"])

@router.get("/", response_model=list[AmigoResponse])
def listar_amigos(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AmigoCore.listar_amigos_com_dados(current_user.id, db)

@router.post("/enviar", response_model=AmizadeResponse)
def enviar_pedido(
    data: AmizadeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AmigoCore.criar_amizade(current_user.id, data.amigo_id, db)

@router.post("/aceitar")
def aceitar_pedido(
    amizade_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AmigoCore.aceitar_amizade(current_user.id, amizade_id, db)

@router.post("/bloquear")
def bloquear_usuario(
    amigo_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AmigoCore.bloquear_usuario(current_user.id, amigo_id, db)

@router.delete("/recusar")
def recusar_pedido(
    amizade_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return AmigoCore.recusar_amizade(current_user.id, amizade_id, db)

if __name__ ==  '__main__':
    pass