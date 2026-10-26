import os
import asyncpg
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

pool = None

async def init_db():
    global pool
    try:
        pool = await asyncpg.create_pool(
            dsn=DATABASE_URL,
            min_size=1,
            max_size=10,
            timeout=30.0
        )
        print("Conexão estabelecida com sucesso com o PostgreSQL (Neon DB)!")
    except Exception as e:
        print(f"Erro ao conectar ao Neon DB: {e}")

async def close_db():
    global pool
    if pool:
        await pool.close()

def get_pool():
    return pool