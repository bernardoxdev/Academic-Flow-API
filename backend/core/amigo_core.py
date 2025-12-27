from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_

from backend.models.amigo import Amizade, StatusAmizade
from backend.models.user import User


class AmigoCore:
    @staticmethod
    def criar_amizade(user_id: int, amigo_id: int, db: Session):
        if user_id == amigo_id:
            raise HTTPException(400, "Não é possível adicionar a si mesmo")

        user_id, amigo_id = sorted([user_id, amigo_id])

        existente = db.query(Amizade).filter(
            Amizade.user_id == user_id,
            Amizade.amigo_id == amigo_id
        ).first()

        if existente:
            raise HTTPException(400, "Amizade já existe")

        amizade = Amizade(
            user_id=user_id,
            amigo_id=amigo_id,
            status=StatusAmizade.pendente
        )

        db.add(amizade)
        db.commit()
        db.refresh(amizade)
        return amizade

    @staticmethod
    def aceitar_amizade(user_id: int, amizade_id: int, db: Session):
        amizade = db.query(Amizade).filter(
            Amizade.id == amizade_id,
            Amizade.status == StatusAmizade.pendente
        ).first()

        if not amizade:
            raise HTTPException(404, "Pedido não encontrado")

        if user_id not in (amizade.user_id, amizade.amigo_id):
            raise HTTPException(403, "Sem permissão")

        amizade.status = StatusAmizade.aceita
        db.commit()
        return amizade

    @staticmethod
    def recusar_amizade(user_id: int, amizade_id: int, db: Session):
        amizade = db.query(Amizade).filter(
            Amizade.id == amizade_id,
            Amizade.status == StatusAmizade.pendente
        ).first()

        if not amizade:
            raise HTTPException(404, "Pedido não encontrado")

        if user_id not in (amizade.user_id, amizade.amigo_id):
            raise HTTPException(403, "Sem permissão")

        db.delete(amizade)
        db.commit()
        return {"detail": "Pedido recusado"}

    @staticmethod
    def bloquear_usuario(user_id: int, amigo_id: int, db: Session):
        user_id, amigo_id = sorted([user_id, amigo_id])

        amizade = db.query(Amizade).filter(
            Amizade.user_id == user_id,
            Amizade.amigo_id == amigo_id
        ).first()

        if not amizade:
            amizade = Amizade(
                user_id=user_id,
                amigo_id=amigo_id,
                status=StatusAmizade.bloqueada
            )
            db.add(amizade)
        else:
            amizade.status = StatusAmizade.bloqueada

        db.commit()
        return {"detail": "Usuário bloqueado"}

    @staticmethod
    def listar_amigos_com_dados(user_id: int, db: Session):
        amizades = (
            db.query(Amizade, User)
            .join(
                User,
                or_(
                    User.id == Amizade.user_id,
                    User.id == Amizade.amigo_id
                )
            )
            .filter(
                Amizade.status == StatusAmizade.aceita,
                or_(
                    Amizade.user_id == user_id,
                    Amizade.amigo_id == user_id
                ),
                User.id != user_id
            )
            .all()
        )

        resultado = []

        for amizade, amigo in amizades:
            resultado.append({
                "amizade_id": amizade.id,
                "status": amizade.status,
                "amigo": amigo
            })

        return resultado