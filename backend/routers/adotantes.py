from fastapi import APIRouter, HTTPException
from backend.database import get_pool

router = APIRouter(prefix="/api", tags=["Adotantes"])

@router.get("/adotante/{id_usuario}")
async def obter_perfil_adotante(id_usuario: int):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    query_adotante = """
        SELECT 
            a.id_usuario,
            a.nome,
            a.cpf,
            a.tipo_residencia,
            u.email,
            u.rua,
            u.numero,
            u.bairro,
            u.cep,
            u.cidade,
            u.estado,
            u.complemento
        FROM adotante a
        JOIN usuario u ON a.id_usuario = u.id_usuario
        WHERE a.id_usuario = $1;
    """

    async with pool.acquire() as conn:
        try:
            adot = await conn.fetchrow(query_adotante, id_usuario)
            if not adot:
                raise HTTPException(status_code=404, detail="Adotante não encontrado.")

            tels_raw = await conn.fetch("SELECT telefone FROM usuario_telefone WHERE id_usuario = $1", id_usuario)
            telefones = [t["telefone"] for t in tels_raw] if tels_raw else []

            historico_raw = await conn.fetch("SELECT descricao FROM adotante_historico_pets WHERE id_usuario = $1", id_usuario)
            historico = " ".join([h["descricao"] for h in historico_raw]) if historico_raw else "Nenhum histórico registrado."

            return {
                "id_usuario": adot["id_usuario"],
                "nome": adot["nome"],
                "cpf": adot["cpf"],
                "tipo_residencia": adot["tipo_residencia"],
                "email": adot["email"],
                "rua": adot["rua"],
                "numero": adot["numero"],
                "bairro": adot["bairro"],
                "cep": adot["cep"],
                "cidade": adot["cidade"],
                "estado": adot["estado"],
                "complemento": adot["complemento"],
                "telefones": telefones,
                "historico_pets": historico
            }
        except HTTPException as h:
            raise h
        except Exception as e:
            print(f"Erro ao obter dados do adotante: {e}")
            raise HTTPException(status_code=500, detail="Erro ao obter perfil do adotante.")
