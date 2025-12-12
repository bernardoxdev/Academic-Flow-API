import os
import polars as pl

from backend.config.paths import PARQUET_DIR
from backend.data.materias_data import NOMES_MATERIAS, MATERIAS_ENUMERADAS, FLUXOGRAMA_MATERIAS

def gerar_data() -> None:
    os.makedirs(PARQUET_DIR, exist_ok=True)

    pl.DataFrame({
        "id": list(MATERIAS_ENUMERADAS.keys()),
        "codigo": list(MATERIAS_ENUMERADAS.values()),
        "nome": [NOMES_MATERIAS[c] for c in MATERIAS_ENUMERADAS.values()]
    }).write_parquet(os.path.join(PARQUET_DIR, "materias.parquet"))

    rows = []
    for m, ps in FLUXOGRAMA_MATERIAS.items():
        for p in ps:
            rows.append({"materia": m, "pre_requisito": p})

    pl.DataFrame(rows).write_parquet(os.path.join(PARQUET_DIR, "prerequisitos.parquet"))
    
if __name__ == '__main__':
    pass