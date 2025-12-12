from fastapi import APIRouter

from backend.core.lazy_loader import LazyLoader

router = APIRouter(prefix="/fluxograma", tags=["Fluxograma"])

@router.get("/")
def fluxograma():
    materias = LazyLoader.materias()
    prereqs = LazyLoader.prerequisitos()

    df = (
        prereqs
        .join(materias, left_on="materia", right_on="codigo")
        .rename({"nome": "materia_nome"})
        .join(materias, left_on="pre_requisito", right_on="codigo")
        .rename({"nome": "prereq_nome"})
        .select(["materia", "materia_nome", "pre_requisito", "prereq_nome"])
        .collect()
    )

    return df.to_dicts()

if __name__ == '__main__':
    pass