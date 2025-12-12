from fastapi import APIRouter, Depends

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

@router.post(
    "/cadastrar_aluno",
    dependencies=[Depends(require_role("monitor", "admin"))]
)
def cadastrar_aluno():
    return {"status": "aluno cadastrado"}

@router.get(
    "/listar_alunos",
    dependencies=[Depends(require_role("admin"))]
)
def listar_alunos():
    return {"alunos": []}

if __name__ == '__main__':
    pass