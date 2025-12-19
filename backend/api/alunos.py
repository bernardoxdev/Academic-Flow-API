from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.models.user import User
from backend.models.schemas import PodeCursarRequest
from backend.core.regras import RegrasAcademicas
from backend.core.security import require_role

router = APIRouter(
    prefix="/alunos",
    tags=["Alunos"]
)

@router.post(
    "/pode-cursar",
    dependencies=[Depends(require_role("aluno", "monitor", "admin"))]
)
def pode_cursar(data: PodeCursarRequest):
    regras = RegrasAcademicas()
    return {
        "pode_cursar": regras.pode_cursar(data.aluno_id, data.materia)
    }

@router.get(
    "/listar-alunos",
    dependencies=[Depends(require_role("admin"))]
)
def listar_alunos(
    db: Session = Depends(get_db)
):
    registros = (
        db.query(User)
        .filter_by(role="aluno")
        .all()
    )
    
    return {"alunos": registros}

if __name__ == '__main__':
    pass