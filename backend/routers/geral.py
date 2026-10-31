from fastapi import APIRouter, HTTPException
from backend.database import get_pool

router = APIRouter(prefix="/api", tags=["Geral e Estatísticas"])

@router.get("/estatisticas")
async def obter_estatisticas():
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    async with pool.acquire() as conn:
        try:
            total_resgatados = await conn.fetchval("SELECT COUNT(*) FROM Animal")
            total_adocoes = await conn.fetchval("SELECT COUNT(*) FROM Adota WHERE status IN ('Aprovada', 'Concluída', 'Aprovado')")
            total_padrinhos = await conn.fetchval("SELECT COUNT(*) FROM Apadrinha WHERE status = 'Ativo'")
            query_ongs = """
                SELECT ROUND((COUNT(CASE WHEN selo_verificacao = TRUE THEN 1 END) * 100.0) / NULLIF(COUNT(*), 0))
                FROM Instituicao
            """
            percentual_ongs = await conn.fetchval(query_ongs)

            return {
                "totalResgatados": f"{total_resgatados or 0}+",
                "adocoesConcluidas": f"{total_adocoes or 0}+",
                "padrinhosAtivos": f"{total_padrinhos or 0}+",
                "ongsVerificadas": f"{int(percentual_ongs) if percentual_ongs is not None else 100}%"
            }
        except Exception as e:
            print(f"Erro na consulta de estatísticas: {e}")
            raise HTTPException(status_code=500, detail="Erro ao consultar o banco de dados")

@router.get("/pets/destaque")
async def obter_pets_destaque():
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    query = """
        SELECT 
            a.id_animal AS id,
            a.nome,
            a.especie,
            a.raca,
            a.idade,
            a.porte,
            a.status,
            i.razao_social AS ong
        FROM Animal a
        INNER JOIN Instituicao i ON a.id_instituicao = i.id_usuario
        WHERE a.status = 'Disponível' OR a.status = 'Em tratamento'
        LIMIT 6;
    """

    async with pool.acquire() as conn:
        try:
            rows = await conn.fetch(query)
            pets_formatados = []
            for row in rows:
                pet = dict(row)
                especie = pet.get("especie", "")
                pet["idade"] = f"{pet['idade']} ano(s)" if pet.get("idade") else "Não informada"
                if especie.lower() == "gato":
                    pet["foto"] = "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&q=80&w=600"
                else:
                    pet["foto"] = "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=600"
                pets_formatados.append(pet)
            return pets_formatados
        except Exception as e:
            print(f"Erro na consulta de pets em destaque: {e}")
            raise HTTPException(status_code=500, detail="Erro ao consultar o banco de dados")

@router.get("/dashboard/estatisticas-brasil")
async def obter_estatisticas_brasil():
    return {
        "animaisSobTutela": "+185 mil",
        "taxaSucesso": "94%",
        "prontuariosAuditados": "100%"
    }
