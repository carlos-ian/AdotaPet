from fastapi import APIRouter, HTTPException
from backend.database import get_pool
from backend.schemas import AdocaoSchema, ApadrinhamentoSchema

router = APIRouter(prefix="/api", tags=["Adoções e Apadrinhamentos"])

@router.get("/adotante/{id_usuario}/adocoes")
async def obter_adocoes_adotante(id_usuario: int):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    query = """
        SELECT 
            ad.id_adotante,
            ad.id_animal,
            ad.status,
            ad.data_de_solicitacao,
            ad.data_de_conclusao,
            ad.observacao_do_processo,
            a.nome as pet_nome,
            a.especie as pet_especie,
            i.razao_social as ong_nome
        FROM adota ad
        JOIN animal a ON ad.id_animal = a.id_animal
        JOIN instituicao i ON a.id_instituicao = i.id_usuario
        WHERE ad.id_adotante = $1
        ORDER BY ad.data_de_solicitacao DESC;
    """

    async with pool.acquire() as conn:
        try:
            rows = await conn.fetch(query, id_usuario)
            return [
                {
                    "id_animal": r["id_animal"],
                    "pet_nome": r["pet_nome"],
                    "pet_especie": r["pet_especie"],
                    "ong_nome": r["ong_nome"],
                    "status": r["status"],
                    "data_solicitacao": r["data_de_solicitacao"].strftime("%d/%m/%Y") if r["data_de_solicitacao"] else "-",
                    "data_conclusao": r["data_de_conclusao"].strftime("%d/%m/%Y") if r["data_de_conclusao"] else "-",
                    "observacoes": r["observacao_do_processo"] or "Em andamento"
                }
                for r in rows
            ]
        except Exception as e:
            print(f"Erro ao consultar adoções do adotante: {e}")
            raise HTTPException(status_code=500, detail="Erro ao consultar adoções.")

@router.get("/adotante/{id_usuario}/apadrinhamentos")
async def obter_apadrinhamentos_adotante(id_usuario: int):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    query = """
        SELECT 
            ap.id_adotante,
            ap.id_animal,
            ap.tipo_de_contribuicao,
            ap.valor_recorrente,
            ap.frequencia,
            ap.status,
            ap.data_de_inicio,
            a.nome as pet_nome,
            a.especie as pet_especie,
            i.razao_social as ong_nome
        FROM apadrinha ap
        JOIN animal a ON ap.id_animal = a.id_animal
        JOIN instituicao i ON a.id_instituicao = i.id_usuario
        WHERE ap.id_adotante = $1
        ORDER BY ap.data_de_inicio DESC;
    """

    async with pool.acquire() as conn:
        try:
            rows = await conn.fetch(query, id_usuario)
            return [
                {
                    "id_animal": r["id_animal"],
                    "pet_nome": r["pet_nome"],
                    "pet_especie": r["pet_especie"],
                    "ong_nome": r["ong_nome"],
                    "tipo_de_contribuicao": r["tipo_de_contribuicao"],
                    "valor_recorrente": float(r["valor_recorrente"]) if r["valor_recorrente"] is not None else 0.0,
                    "frequencia": r["frequencia"],
                    "status": r["status"],
                    "data_de_inicio": r["data_de_inicio"].strftime("%d/%m/%Y") if r["data_de_inicio"] else "-"
                }
                for r in rows
            ]
        except Exception as e:
            print(f"Erro ao consultar apadrinhamentos do adotante: {e}")
            raise HTTPException(status_code=500, detail="Erro ao consultar apadrinhamentos.")

@router.post("/adocao")
async def submeter_adocao(dados: AdocaoSchema):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")
    query = """
        INSERT INTO adota (id_adotante, id_animal, status, data_de_solicitacao, observacao_do_processo, data_inclusao)
        VALUES ($1, $2, 'Em Análise', CURRENT_DATE, $3, NOW())
        ON CONFLICT (id_adotante, id_animal) 
        DO UPDATE SET status = 'Em Análise', data_de_solicitacao = CURRENT_DATE, observacao_do_processo = EXCLUDED.observacao_do_processo, data_alteracao = NOW();
    """
    async with pool.acquire() as conn:
        try:
            await conn.execute(query, dados.id_adotante, dados.id_animal, dados.observacao)
            return {"mensagem": "Solicitação de adoção registrada com sucesso!"}
        except Exception as e:
            print(f"Erro ao registrar adoção: {e}")
            raise HTTPException(status_code=500, detail="Erro ao registrar solicitação de adoção.")

@router.post("/apadrinhamento")
async def submeter_apadrinhamento(dados: ApadrinhamentoSchema):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")
    query = """
        INSERT INTO apadrinha (id_adotante, id_animal, tipo_de_contribuicao, valor_recorrente, frequencia, status, data_de_inicio)
        VALUES ($1, $2, $3, $4, $5, 'Ativo', CURRENT_DATE)
        ON CONFLICT (id_adotante, id_animal)
        DO UPDATE SET tipo_de_contribuicao = EXCLUDED.tipo_de_contribuicao, valor_recorrente = EXCLUDED.valor_recorrente, frequencia = EXCLUDED.frequencia, status = 'Ativo', data_de_inicio = CURRENT_DATE;
    """
    async with pool.acquire() as conn:
        try:
            await conn.execute(query, dados.id_adotante, dados.id_animal, dados.tipo_de_contribuicao, dados.valor_recorrente, dados.frequencia)
            return {"mensagem": "Vínculo de apadrinhamento registrado com sucesso!"}
        except Exception as e:
            print(f"Erro ao registrar apadrinhamento: {e}")
            raise HTTPException(status_code=500, detail="Erro ao registrar apadrinhamento.")
