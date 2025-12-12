import os
import polars as pl

from backend.config.paths import PARQUET_DIR

class LazyLoader:
    @staticmethod
    def materias() -> pl.LazyFrame:
        return pl.scan_parquet(os.path.join(PARQUET_DIR, "materias.parquet"))

    @staticmethod
    def prerequisitos() -> pl.LazyFrame:
        return pl.scan_parquet(os.path.join(PARQUET_DIR, "prerequisitos.parquet"))

    @staticmethod
    def notas() -> pl.LazyFrame:
        return pl.scan_parquet(os.path.join(PARQUET_DIR, "notas.parquet"))
    
if __name__ == '__main__':
    pass