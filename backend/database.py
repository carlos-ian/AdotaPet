import os
from pathlib import Path
import asyncpg
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")
load_dotenv(BASE_DIR.parent / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
pool = None

async def init_db():
    global pool
    if not DATABASE_URL:
        print("❌ DATABASE_URL não encontrada no ficheiro .env")
        return
    try:
        url = DATABASE_URL.strip().strip("'").strip('"')
        
        if url.startswith("postgres://"):
            url = url.replace("postgres://", "postgresql://", 1)
            
        if "?sslmode=" in url:
            url = url.split("?sslmode=")[0]
        elif "&sslmode=" in url:
            url = url.split("&sslmode=")[0]

        # statement_cache_size=0 desativa o cache de prepared statements do asyncpg,
        # resolvendo definitivamente o erro 'inconsistent types deduced for parameter $1' no Neon DB.
        pool = await asyncpg.create_pool(
            dsn=url,
            ssl="require",
            min_size=1,
            max_size=10,
            statement_cache_size=0
        )
        print("✅ Conexão estabelecida com sucesso com o PostgreSQL (Neon DB)!")
    except Exception as e:
        print(f"❌ Erro ao conectar ao banco de dados: {e}")

async def close_db():
    global pool
    if pool:
        await pool.close()
        print("🔒 Conexão com o banco de dados encerrada.")

def get_pool():
    return pool