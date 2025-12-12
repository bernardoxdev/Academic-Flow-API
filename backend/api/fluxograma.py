from fastapi import APIRouter, Query
import polars as pl

from backend.core.lazy_loader import LazyLoader
from backend.core.grafo import coletar_prerequisitos

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
        .group_by(["materia", "materia_nome"])
        .agg(
            pl.struct(
                pl.col("pre_requisito").alias("codigo"),
                pl.col("prereq_nome").alias("nome")
            ).alias("pre_requisitos")
        )
        .collect()
    )

    return df.to_dicts()

@router.get("/requisitos-completos")
def requisitos_completos(codigo: str = Query(...)):
    prereqs_df = LazyLoader.prerequisitos().collect()
    materias_df = LazyLoader.materias().collect()

    mapa = {}
    for row in prereqs_df.iter_rows(named=True):
        materia = row["materia"]
        prereq = row["pre_requisito"]
        mapa.setdefault(materia, []).append(prereq)
    
    todos = coletar_prerequisitos(mapa, codigo)

    if not todos:
        return {
            "materia": codigo,
            "pre_requisitos": []
        }
        
    resultado = (
        materias_df
        .filter(pl.col("codigo").is_in(list(todos)))
        .select(["codigo", "nome"])
        .to_dicts()
    )
    
    return {
        "materia": codigo,
        "quantidade": len(resultado),
        "pre_requisitos": resultado
    }

if __name__ == "__main__":
    pass