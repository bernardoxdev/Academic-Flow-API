from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from backend.core.limiter import limiter
from backend.data.seed import criar_admin_se_nao_existir

from backend.api.auth import router as auth_router
from backend.api.alunos import router as alunos_router
from backend.api.fluxograma import router as fluxograma_router
from backend.api.data_materias import router as data_materias_router
from backend.api.atividades import router as atividades_router
from backend.api.boca import router as boca_router

from backend.core.database import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Academic Flow API",
    summary="API para gerenciamento acadêmico e fluxograma de disciplinas",
    description="""
    API responsável por fornecer dados acadêmicos como:
    - Sistema de Login e Autenticação [OK]
    - Fluxograma do curso [90/100]
    - Pré-requisitos de disciplinas [80/100]
    - Validação de matrícula de alunos [0/100]
    - Classificação da dificuldade das matérias [0/100]
    - Dados sobre as matérias [0/100]
    - Gerar listas de atividades [0/100]
    - Resolver exercícios da plataforma BOCA [0/100]
    
    Desenvolvida para o projeto Academic Flow.
    
    Um projeto de ALUNOS para ALUNOS.
    """,
    version="BETA"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "http://127.0.0.1:5000",
        "http://localhost:5000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )
    
@app.on_event("startup")
def startup():
    criar_admin_se_nao_existir()

app.include_router(auth_router)
app.include_router(alunos_router)
app.include_router(fluxograma_router)
app.include_router(data_materias_router)
app.include_router(atividades_router)
app.include_router(boca_router)

if __name__ == '__main__':
    pass
