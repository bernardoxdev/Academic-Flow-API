import polars as pl

from backend.core.lazy_loader import LazyLoader

class RegrasAcademicas:
    MEDIA_MINIMA = 60

    def pode_cursar(self, aluno_id: int, materia: str) -> bool:
        prereqs = (
            LazyLoader.prerequisitos()
            .filter(pl.col("materia") == materia)
            .select("pre_requisito")
            .collect()
            .to_series()
            .to_list()
        )

        if not prereqs:
            return True

        aprovadas = (
            LazyLoader.notas()
            .filter(pl.col("aluno_id") == aluno_id)
            .filter(pl.col("media") >= self.MEDIA_MINIMA)
            .filter(pl.col("materia").is_in(prereqs))
            .select("materia")
            .collect()
            .to_series()
            .to_list()
        )

        return set(prereqs) == set(aprovadas)

if __name__ == '__main__':
    pass