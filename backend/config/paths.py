import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

PARQUET_DIR = os.path.join(BASE_DIR, "data_store", "parquet")
DB_DIR = os.path.join(BASE_DIR, "data_store", "db")