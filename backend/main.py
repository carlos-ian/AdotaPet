from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.database import init_db, close_db
from backend.routers import auth, animais, processos, instituicoes, adotantes, prontuarios, geral

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(
    title="AdotaPet API",
    description="API RESTful para o Sistema de Gestão de Processos de Adoção e Apadrinhamento de Animais",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Conexão de todos os roteadores modulares
app.include_router(geral.router)
app.include_router(auth.router)
app.include_router(animais.router)
app.include_router(processos.router)
app.include_router(instituicoes.router)
app.include_router(adotantes.router)
app.include_router(prontuarios.router)
