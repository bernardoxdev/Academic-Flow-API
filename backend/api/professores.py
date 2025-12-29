from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from backend.models.professor import Professor
from backend.models.disciplinas_professor import DisciplinaProfessor
from backend.core.database import get_db
from backend.core.security import require_role
from backend.models.schemas import (
    AdicionarProfessor,
    AtualizarProfessor
)
from backend.models.return_schemas import (
    ProfessoresListarReturn,
    Status
)

router = APIRouter(
    prefix="/professores",
    tags=["Professores"]
)

@router.get(
    '/', status_code=status.HTTP_200_OK,
    response_model=ProfessoresListarReturn,
    summary="Listar todos os professores",
    description="Retorna uma lista de todos os professores cadastrados no sistema."
)
def listar_professores(
    db: Session = Depends(get_db)
):
    resultados = (
        db.query(Professor, DisciplinaProfessor)
        .outerjoin(
            DisciplinaProfessor,
            Professor.id == DisciplinaProfessor.id_professor
        )
        .all()
    )

    response = []
    for professor, disciplina in resultados:
        response.append({
            "id_professor": professor.id,
            "nome": professor.nome,
            "email": professor.email,
            "departamento": professor.departamento,
            "id_disciplina": disciplina.id_disciplina if disciplina else None
        })
    
    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum professor encontrado."
        )
        
    return ProfessoresListarReturn(professores=response)

@router.post(
    '/', status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(require_role("admin", "monitor"))],
    response_model=Status,
    summary="Adicionar um novo professor",
    description="Adiciona um novo professor ao sistema."
)
def adicionar_professor(
    data: AdicionarProfessor,
    db: Session = Depends(get_db)
):
    novo_professor = Professor(
        nome=data.nome,
        email=data.email,
        departamento=data.departamento
    )
    db.add(novo_professor)
    db.commit()
    db.refresh(novo_professor)

    return Status(message="Professor adicionado com sucesso.")

@router.put(
    '/atualizar', status_code=status.HTTP_200_OK,
    dependencies=[Depends(require_role("admin", "monitor", "professor"))],
    response_model=dict,
    summary="Atualizar informações do professor",
    description="Atualiza as informações de um professor específico."
)
def atualizar_professor(
    data: AtualizarProfessor,
    db: Session = Depends(get_db)
):
    professor = db.query(Professor).filter(Professor.id == data.id).first()
    
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor não encontrado."
        )
        
    professor.nome = data.nome
    professor.email = data.email
    professor.departamento = data.departamento
    
    db.commit()
    db.refresh(professor)
    
    if data.disciplinas:
        db.query(DisciplinaProfessor).filter(
            DisciplinaProfessor.id_professor == professor.id
        ).delete()
        
        for disciplina_id in data.disciplinas:
            nova_relacao = DisciplinaProfessor(
                id_professor=professor.id,
                id_disciplina=disciplina_id
            )
            
            db.add(nova_relacao)
        
        db.commit()
    
    return Status(status="Professor atualizado com sucesso.")

@router.delete(
    '/{professor_id}', status_code=status.HTTP_204_NO_CONTENT,
    summary="Remover um professor",
    description="Remove um professor específico do sistema."
)
def remover_professor(
    professor_id: int,
    db: Session = Depends(get_db)
):
    professor = db.query(Professor).filter(Professor.id == professor_id).first()
    
    if not professor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Professor não encontrado."
        )
        
    db.delete(professor)
    db.commit()
    
    return

if __name__ == '__main__':
    pass