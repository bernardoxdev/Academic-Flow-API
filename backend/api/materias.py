import polars as pl

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.core.database import get_db
from backend.core.lazy_loader import LazyLoader
from backend.core.security import (
    get_current_user,
    require_role
)
from backend.models.user import User
from backend.models.comentario_materia import ComentarioMateria
from backend.models.nota_materia import NotaMateria
from backend.models.dificuldade_materia import DificuldadeMateria
from backend.models.fazendo_materia import FazendoMateria
from backend.models.aluno_materia import AlunoMateria
from backend.models.schemas import (
    MateriaFazendo,
    AdicionarComentario,
    AtualizarComentario,
    DeletarComentario,
    AdicionarDificuldade,
    AtualizarDificuldade,
    RemoverDificuldade,
    AdicionarNota,
    AtualizarNota,
    RemoverNota
)

router = APIRouter(
    prefix="/materias",
    tags=["Dados das Matérias"]
)

@router.get(
    '/', status_code=status.HTTP_200_OK,
    summary="Listar todas as matérias",
    description="Retorna a lista de todas as matérias disponíveis",
    dependencies=[Depends(require_role("aluno"))]
)
def index():
    materias = LazyLoader.materias()
    
    df = (
        materias.
        select([
            pl.col("codigo").alias("id"),
            pl.col("nome")
        ])
    )
    
    if df.is_empty():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="nenhuma matéria encontrada")
    
    return df.to_dicts()
    
@router.get(
    '/fazendo', status_code=status.HTTP_200_OK,
    summary="Listar matérias que o aluno está fazendo",
    description="Retorna a lista de matérias que o aluno autenticado está fazendo",
    dependencies=[Depends(require_role("aluno"))]
)
def get_fazendo(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    aluno_id = current_user.id
    
    registro = (
        db.query(FazendoMateria)
        .filter_by(
            aluno_id=aluno_id,
            fazendo=True
        )
        .all()
    )
    
    if not registro:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="não encontrado")
    
    materias_fazendo = [ registro.id_materia for registro in registro ]
    
    return {
        "materias": materias_fazendo
    }

@router.get(
    '/comentarios', status_code=status.HTTP_200_OK,
    summary="Listar comentários do aluno",
    description="Retorna a lista de comentários feitos pelo aluno autenticado",
    dependencies=[Depends(require_role("aluno"))]
)
def get_comentarios(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    aluno_id = current_user.id
    
    registro = (
        db.query(ComentarioMateria)
        .filter_by(
            aluno_id=aluno_id
        )
        .all()
    )
    
    if not registro:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="não encontrado")
    
    comentarios = {}
    
    for r in registro:
        comentarios[r.id_materia] = r.comentario    
    
    return {"comentarios": comentarios}

@router.get(
    "/comentarios/todos", status_code=status.HTTP_200_OK,
    summary="Listar todos os comentários",
    description="Retorna a lista de todos os comentários feitos por todos os alunos"
)
def get_todos_comentarios(
    db: Session = Depends(get_db)
):
    registros = db.query(ComentarioMateria).all()

    if not registros:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum comentário encontrado"
        )

    comentarios = {}

    for r in registros:
        if r.comentario:
            if r.id_aluno not in comentarios:
                comentarios[r.id_aluno] = {}

            comentarios[r.id_aluno][r.id_materia] = r.comentario

    comentarios = {k: v for k, v in comentarios.items() if v}

    if not comentarios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum comentário válido encontrado"
        )

    return {"comentarios": comentarios}

@router.get(
    "/comentarios/todos/materia", status_code=status.HTTP_200_OK,
    summary="Listar todos os comentários de uma matéria específica",
    description="Retorna a lista de todos os comentários feitos por todos os alunos para uma matéria específica"
)
def get_todos_comentarios_materia(
    id_materia: int,
    db: Session = Depends(get_db)
):
    registros = (
        db.query(ComentarioMateria)
        .filter_by(id_materia=id_materia)
        .all()
    )

    if not registros:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum comentário encontrado para a matéria especificada"
        )

    comentarios = {}

    for r in registros:
        if r.comentario:
            comentarios[r.id_aluno] = r.comentario

    if not comentarios:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum comentário válido encontrado para a matéria especificada"
        )

    return {"comentarios": comentarios}

@router.get(
    '/dificuldades', status_code=status.HTTP_200_OK,
    summary="Lista o nível de dificuldade das matérias do aluno",
    description="Retorna o nível de dificuldade que o aluno autenticado atribuiu às matérias",
    dependencies=[Depends(require_role("aluno"))]
)
def get_dificuldades(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    aluno_id = current_user.id
    
    registro = (
        db.query(DificuldadeMateria)
        .filter_by(
            aluno_id=aluno_id
        )
        .all()
    )
    
    if not registro:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="não encontrado")
    
    dificuldades = {}
    
    for r in registro:
        dificuldades[r.id_materia] = r.dificuldade    
    
    return dificuldades

@router.get(
    '/notas', status_code=status.HTTP_200_OK,
    summary="Lista as notas das matérias do aluno",
    description="Retorna as notas que o aluno autenticado atribuiu às matérias",
    dependencies=[Depends(require_role("aluno"))]
)
def get_notas(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    aluno_id = current_user.id
    
    registro = (
        db.query(NotaMateria)
        .filter_by(
            aluno_id=aluno_id
        )
        .all()
    )
    
    if not registro:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="não encontrado")
    
    notas = {}
    
    for r in registro:
        notas[r.id_materia] = r.nota    
    
    return notas

@router.get(
    '/faltando', status_code=status.HTTP_200_OK,
    summary="Listar matérias faltando para o aluno",
    description="Retorna a lista de matérias que o aluno autenticado ainda não concluiu",
    dependencies=[Depends(require_role("aluno"))]
)
def get_faltando(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    aluno_id = current_user.id
    
    registro = (
        db.query(AlunoMateria)
        .filter_by(
            aluno_id=aluno_id,
            concluida=False
        )
        .all()
    )
    
    if not registro:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="não encontrado")
    
    materias_faltando = [ registro.materia_codigo for registro in registro ]
    
    return {
        "materias": materias_faltando
    }

@router.post(
    '/marcar-fazendo', status_code=status.HTTP_200_OK,
    summary="Marcar matéria como sendo feita",
    description="Marca uma matéria como sendo feita pelo aluno autenticado",
    dependencies=[Depends(require_role("aluno"))]
)
def marcar_get(
    data: MateriaFazendo,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    aluno_id = current_user.id
    
    registro = (
        db.query(FazendoMateria)
        .filter_by(
            aluno_id=aluno_id,
            id_materia=data.id_materia
        )
        .first()
    )
    
    if not registro:
        registro = FazendoMateria(
            id_materia=data.id_materia,
            id_aluno=aluno_id,
            fazendo=True
        )
        db.add(registro)
    else:
        registro.fazendo = True
        
    db.commit()
    
    return {"status": "ok"}

@router.post(
    '/desmarcar-fazendo', status_code=status.HTTP_200_OK,
    summary="Desmarcar matéria como sendo feita",
    description="Desmarca uma matéria como sendo feita pelo aluno autenticado",
    dependencies=[Depends(require_role("aluno"))]
)
def desmarcar_get(
    data: MateriaFazendo,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    aluno_id = current_user.id
    
    registro = (
        db.query(FazendoMateria)
        .filter_by(
            aluno_id=aluno_id,
            id_materia=data.id_materia
        )
        .first()
    )
    
    if not registro:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="não encontrado")
    
    registro.fazendo = False
    db.commit()
    
    return {"status": "ok"}

@router.post(
    '/adicionar-comentario', status_code=status.HTTP_201_CREATED,
    summary="Adicionar comentário a uma matéria",
    description="Adiciona um comentário a uma matéria pelo aluno autenticado",
    dependencies=[Depends(require_role("aluno"))]
)
def adicionar_comentario(
    data: AdicionarComentario,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    aluno_id = current_user.id
    
    registro = (
        db.query(ComentarioMateria)
        .filter_by(
            aluno_id=aluno_id,
            id_materia=data.id_materia
        )
        .first()
    )
    
    if registro:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="já existe")
    
    registro = ComentarioMateria(
        id_materia=data.id_materia,
        id_aluno=aluno_id,
        comentario=data.comentario
    )
    db.add(registro)
    db.commit()
    
    return {"status": "ok"}

@router.post(
    '/deletar-comentario', status_code=status.HTTP_200_OK,
    summary="Deletar comentário de uma matéria",
    description="Deleta um comentário de uma matéria feito pelo aluno autenticado",
    dependencies=[Depends(require_role("aluno"))]
)
def deletar_comentario(
    data: DeletarComentario,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    aluno_id = current_user.id
    
    registro = (
        db.query(ComentarioMateria)
        .filter_by(
            id=data.id_comentario,
            id_aluno=aluno_id
        )
        .first()
    )
    
    if not registro:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="não encontrado")
    
    db.delete()
    db.commit()
    
    return {"status": "ok"}

@router.post(
    '/atualizar-comentario', status_code=status.HTTP_200_OK,
    summary="Atualizar comentário de uma matéria",
    description="Atualiza um comentário de uma matéria feito pelo aluno autenticado",
    dependencies=[Depends(require_role("aluno"))]
)
def atualizar_comentario(
    data: AtualizarComentario,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    aluno_id = current_user.id
    
    registro = (
        db.query(ComentarioMateria)
        .filter_by(
            aluno_id=aluno_id,
            id_materia=data.id_materia
        )
        .first()
    )
    
    if not registro:
        return 
    
    registro.comentario = data.comentario
        
    db.commit()
    
    return {"status": "ok"}

@router.post(
    '/adicionar-nota', status_code=status.HTTP_201_CREATED,
    summary="Adicionar nota a uma matéria",
    description="Adiciona uma nota a uma matéria pelo aluno autenticado",
    dependencies=[Depends(require_role("aluno"))]
)
def adicionar_nota(
    data: AdicionarNota,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    aluno_id = current_user.id
    
    registro = (
        db.query(NotaMateria)
        .filter_by(
            aluno_id=aluno_id,
            id_materia=data.id_materia
        )
        .first()
    )
    
    if registro:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="já existe")    
        
    registro = NotaMateria(
        id_materia=data.id_materia,
        id_aluno=aluno_id,
        nota=data.nota
    )
    db.add(registro)
    db.commit()
    
    return {"status": "ok"}

@router.post(
    '/deletar-nota', status_code=status.HTTP_200_OK,
    summary="Deletar nota de uma matéria",
    description="Deleta uma nota de uma matéria feita pelo aluno autenticado",
    dependencies=[Depends(require_role("aluno"))]
)
def deletar_nota(
    data: RemoverNota,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    aluno_id = current_user.id
    
    registro = (
        db.query(NotaMateria)
        .filter_by(
            id=data.id_nota,
            id_aluno=aluno_id
        )
        .first()
    )
    
    if not registro:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="não encontrado")
    
    db.delete()
    db.commit()
    
    return {"status": "ok"}

@router.post(
    '/atualizar-nota', status_code=status.HTTP_200_OK,
    summary="Atualizar nota de uma matéria",
    description="Atualiza uma nota de uma matéria feita pelo aluno autenticado",
    dependencies=[Depends(require_role("aluno"))]
)
def atualizar_nota(
    data: AtualizarNota,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    aluno_id = current_user.id
    
    registro = (
        db.query(NotaMateria)
        .filter_by(
            id=data.id_nota,
            id_aluno=aluno_id
        )
        .first()
    )
    
    if not registro:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="não encontrado")
    
    registro.nota = data.nova_nota
    
    db.commit()
    
    return {"status": "ok"}

@router.post(
    '/adicionar-dificuldade', status_code=status.HTTP_201_CREATED,
    summary="Adicionar dificuldade a uma matéria",
    description="Adiciona uma dificuldade a uma matéria pelo aluno autenticado",
    dependencies=[Depends(require_role("aluno"))]
)
def adicionar_dificuldade(
    data: AdicionarDificuldade,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    aluno_id = current_user.id
    
    registro = (
        db.query(DificuldadeMateria)
        .filter_by(
            aluno_id=aluno_id,
            id_materia=data.id_materia
        )
        .first()
    )
    
    if registro:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="já existe")    
        
    registro = DificuldadeMateria(
        id_materia=data.id_materia,
        id_aluno=aluno_id,
        dificuldade=data.dificuldade
    )
    db.add(registro)
    db.commit()
    
    return {"status": "ok"}

@router.post(
    '/deletar-dificuldade', status_code=status.HTTP_200_OK,
    summary="Deletar dificuldade de uma matéria",
    description="Deleta uma dificuldade de uma matéria feita pelo aluno autenticado",
    dependencies=[Depends(require_role("aluno"))]
)
def deletar_dificuldade(
    data: RemoverDificuldade,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    aluno_id = current_user.id
    
    registro = (
        db.query(DificuldadeMateria)
        .filter_by(
            id=data.id_dificuldade,
            id_aluno=aluno_id
        )
        .first()
    )
    
    if not registro:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="não encontrado")
    
    db.delete()
    db.commit()
    
    return {"status": "ok"}

@router.post(
    '/atualizar-dificuldade', status_code=status.HTTP_200_OK,
    summary="Atualizar dificuldade de uma matéria",
    description="Atualiza uma dificuldade de uma matéria feita pelo aluno autenticado",
    dependencies=[Depends(require_role("aluno"))]
)
def atualizar_dificuldade(
    data: AtualizarDificuldade,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    aluno_id = current_user.id
    
    registro = (
        db.query(DificuldadeMateria)
        .filter_by(
            id=data.id_dificuldade,
            id_aluno=aluno_id
        )
        .first()
    )
    
    if not registro:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="não encontrado")
    
    registro.dificuldade = data.nova_dificuldade
    
    db.commit()
    
    return {"status": "ok"}

if __name__ == '__main__':
    pass