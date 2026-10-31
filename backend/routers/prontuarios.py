from fastapi import APIRouter, HTTPException
from backend.database import get_pool
from backend.schemas import ProntuarioSchema
import datetime

router = APIRouter(prefix="/api", tags=["Prontuários"])

@router.get("/prontuario/{id_animal}")
async def obter_prontuario_animal(id_animal: int):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    query_animal = "SELECT id_animal, nome, especie, raca, id_instituicao FROM animal WHERE id_animal = $1;"
    query_pront = """
        SELECT data_procedimento, tipo_procedimento, descricao
        FROM prontuario_veterinario
        WHERE id_animal = $1
        ORDER BY data_procedimento DESC;
    """
    async with pool.acquire() as conn:
        try:
            pet = await conn.fetchrow(query_animal, id_animal)
            if not pet:
                raise HTTPException(status_code=404, detail="Animal não encontrado.")
            records = await conn.fetch(query_pront, id_animal)
            return {
                "pet": dict(pet),
                "registros": [
                    {
                        "data": r["data_procedimento"].strftime("%d/%m/%Y") if r["data_procedimento"] else "-",
                        "data_iso": r["data_procedimento"].strftime("%Y-%m-%d") if r["data_procedimento"] else "",
                        "tipo": r["tipo_procedimento"],
                        "descricao": r["descricao"] or ""
                    } for r in records
                ]
            }
        except HTTPException as h:
            raise h
        except Exception as e:
            print(f"Erro ao obter prontuário: {e}")
            raise HTTPException(status_code=500, detail="Erro ao carregar prontuário.")

@router.post("/prontuario")
async def criar_registro_prontuario(dados: ProntuarioSchema):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    # Tratamento da data: usa data_procedimento fornecida ou data atual
    if dados.data_procedimento and dados.data_procedimento.strip():
        try:
            data_proc = datetime.date.fromisoformat(dados.data_procedimento.strip())
        except ValueError:
            data_proc = datetime.date.today()
    else:
        data_proc = datetime.date.today()

    query = """
        INSERT INTO prontuario_veterinario (id_animal, data_procedimento, tipo_procedimento, descricao)
        VALUES ($1, $2, $3, $4)
        ON CONFLICT (id_animal, data_procedimento, tipo_procedimento)
        DO UPDATE SET descricao = EXCLUDED.descricao;
    """
    async with pool.acquire() as conn:
        try:
            await conn.execute(query, dados.id_animal, data_proc, dados.tipo_procedimento.strip(), dados.descricao)
            return {"mensagem": "Registro adicionado ao prontuário com sucesso!"}
        except Exception as e:
            print(f"Erro ao adicionar prontuário: {e}")
            raise HTTPException(status_code=500, detail=f"Erro ao gravar ficha clínica: {str(e)}")

@router.delete("/prontuario/{id_animal}")
async def excluir_registro_prontuario(id_animal: int, data: str, tipo: str):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    try:
        data_proc = datetime.date.fromisoformat(data.strip())
    except ValueError:
        raise HTTPException(status_code=400, detail="Data em formato inválido. Use AAAA-MM-DD.")

    query = """
        DELETE FROM prontuario_veterinario 
        WHERE id_animal = $1 AND data_procedimento = $2 AND tipo_procedimento = $3;
    """
    async with pool.acquire() as conn:
        try:
            await conn.execute(query, id_animal, data_proc, tipo.strip())
            return {"mensagem": "Registro do prontuário removido com sucesso!"}
        except Exception as e:
            print(f"Erro ao remover registro do prontuário: {e}")
            raise HTTPException(status_code=500, detail="Erro ao excluir registro do prontuário.")
