from fastapi import FastAPI
from fastapi.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

from backend.core.limiter import limiter
from backend.api.auth import router as auth_router
from backend.api.alunos import router as alunos_router
from backend.api.fluxograma import router as fluxograma_router

app = FastAPI(
    title="Academic Flow API",
    summary="API para gerenciamento acadêmico e fluxograma de disciplinas",
    description="""
    API responsável por fornecer dados acadêmicos como:
    - Fluxograma do curso [0/100]
    - Pré-requisitos de disciplinas [0/100]
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

app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)

@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request, exc):
    return JSONResponse(
        status_code=429,
        content={"detail": "Rate limit exceeded"}
    )

app.include_router(auth_router)
app.include_router(alunos_router)
app.include_router(fluxograma_router)

if __name__ == '__main__':
    pass
