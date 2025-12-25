from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.models.user import User
from backend.models.schemas import (
    PodeCursarRequest,
    PodeCursarAlunoRequest
)
from backend.core.regras import RegrasAcademicas
from backend.core.security import (
    require_role,
    get_current_user
)
from backend.models.return_schemas import (
    Alunos,
    PodeCursar
)

router = APIRouter(
    prefix="/alunos",
    tags=["Alunos"]
)

@router.get(
    "/listar-alunos", status_code=status.HTTP_200_OK,
    response_model=Alunos,
    summary="Listar todos os alunos",
    description="Retorna a lista de todos os alunos cadastrados",
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
    
    return Alunos(alunos=registros)

@router.post(
    "/pode-cursar", status_code=status.HTTP_200_OK,
    response_model=PodeCursar,
    summary="Verificar se um aluno pode cursar uma matéria",
    description="Verifica se um aluno pode cursar uma determinada matéria",
    dependencies=[Depends(require_role("monitor", "admin"))]
)
def pode_cursar(
    data: PodeCursarRequest,
    current_user: User = Depends(get_current_user)
):
    regras = RegrasAcademicas()
    
    aluno_id = current_user.id
    
    if data.aluno_id:
        aluno_id = data.aluno_id
    
    return PodeCursar(pode_cursar=regras.pode_cursar(aluno_id, data.materia))

@router.post(
    "/pode-cursar", status_code=status.HTTP_200_OK,
    summary="Verificar se o aluno autenticado pode cursar uma matéria",
    description="Verifica se o aluno autenticado pode cursar uma determinada matéria",
    dependencies=[Depends(require_role("aluno"))]
)
def pode_cursar(
    data: PodeCursarAlunoRequest,
    current_user: User = Depends(get_current_user)
):
    regras = RegrasAcademicas()
    
    return PodeCursar(pode_cursar=regras.pode_cursar(current_user.id, data.materia))

if __name__ == '__main__':
    pass