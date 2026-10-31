from fastapi import APIRouter, HTTPException
from backend.database import get_pool
from backend.schemas import PetSchema
import datetime

router = APIRouter(prefix="/api", tags=["Animais"])

@router.get("/animais")
async def listar_animais(busca: str = None, especie: str = None, porte: str = None, sexo: str = None, status: str = None):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    query = """
        SELECT 
            a.id_animal,
            a.nome,
            a.especie,
            a.raca,
            a.idade,
            a.porte,
            a.sexo,
            a.status as status_db,
            a.observacao,
            i.id_usuario as id_instituicao,
            i.razao_social as instituicao,
            i.selo_verificacao as ong_verificada,
            u.cidade,
            u.estado,
            (SELECT COUNT(*) FROM apadrinha ap WHERE ap.id_animal = a.id_animal AND ap.status = 'Ativo') as padrinhos_ativos,
            (SELECT COUNT(*) FROM adota ad WHERE ad.id_animal = a.id_animal AND ad.status IN ('Aprovada', 'Aprovado')) as adocoes_aprovadas
        FROM animal a
        LEFT JOIN instituicao i ON a.id_instituicao = i.id_usuario
        LEFT JOIN usuario u ON i.id_usuario = u.id_usuario
        ORDER BY a.id_animal;
    """

    async with pool.acquire() as conn:
        try:
            rows = await conn.fetch(query)
            resultado = []
            
            fotos_especies = {
                "cão": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=600&q=80",
                "gato": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=600&q=80",
                "coelho": "https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?auto=format&fit=crop&w=600&q=80",
                "ave": "https://images.unsplash.com/photo-1522858547137-f1dcec554f55?auto=format&fit=crop&w=600&q=80",
                "papagaio": "https://images.unsplash.com/photo-1552728089-57bdde30beb3?auto=format&fit=crop&w=600&q=80",
                "calopsita": "https://images.unsplash.com/photo-1522858547137-f1dcec554f55?auto=format&fit=crop&w=600&q=80",
                "hamster": "https://images.unsplash.com/photo-1548767797-d8c844163c4c?auto=format&fit=crop&w=600&q=80",
                "porquinho-da-índia": "https://images.unsplash.com/photo-1548767797-d8c844163c4c?auto=format&fit=crop&w=600&q=80"
            }

            for r in rows:
                padrinhos = r["padrinhos_ativos"]
                adocoes = r["adocoes_aprovadas"]
                st_db = (r["status_db"] or "").lower()
                
                if "adotado" in st_db or adocoes > 0:
                    status_bloco = "Adotado"
                elif padrinhos > 0:
                    status_bloco = "Ambos"
                else:
                    status_bloco = "Adoção"

                esp = (r["especie"] or "").lower()
                foto_url = fotos_especies.get(esp, "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=600&q=80")
                
                if "golden" in (r["raca"] or "").lower():
                    foto_url = "https://images.unsplash.com/photo-1552053831-71594a27632d?auto=format&fit=crop&w=600&q=80"
                elif "siamês" in (r["raca"] or "").lower():
                    foto_url = "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=600&q=80"
                elif "persa" in (r["raca"] or "").lower():
                    foto_url = "https://images.unsplash.com/photo-1573865526739-10659fec78a5?auto=format&fit=crop&w=600&q=80"

                item = {
                    "id_animal": r["id_animal"],
                    "nome": r["nome"],
                    "especie": r["especie"],
                    "raca": r["raca"],
                    "idade": r["idade"],
                    "porte": r["porte"],
                    "sexo": r["sexo"],
                    "status": status_bloco,
                    "status_original": r["status_db"],
                    "observacao": r["observacao"],
                    "instituicao": r["instituicao"] or "Instituição Parceira",
                    "id_instituicao": r["id_instituicao"],
                    "cidade": r["cidade"],
                    "estado": r["estado"],
                    "ong_verificada": r["ong_verificada"],
                    "foto": foto_url
                }

                if busca:
                    b = busca.lower()
                    if not (b in item["nome"].lower() or b in (item["raca"] or "").lower() or b in item["instituicao"].lower()):
                        continue
                if especie and item["especie"].lower() != especie.lower():
                    if not (especie.lower() == "ave" and item["especie"].lower() in ["ave", "papagaio", "calopsita"]):
                        continue
                if porte and (item["porte"] or "").lower() != porte.lower():
                    continue
                if sexo and (item["sexo"] or "").upper() != sexo.upper():
                    continue
                if status and item["status"].lower() != status.lower():
                    continue

                resultado.append(item)

            return resultado
        except Exception as e:
            print(f"Erro ao listar animais: {e}")
            raise HTTPException(status_code=500, detail="Erro ao consultar animais.")

@router.get("/animais/{id_animal}")
async def obter_detalhes_animal(id_animal: int):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    query_animal = """
        SELECT 
            a.id_animal,
            a.nome,
            a.especie,
            a.raca,
            a.idade,
            a.porte,
            a.sexo,
            a.status as status_db,
            a.observacao,
            i.id_usuario as id_instituicao,
            i.razao_social as instituicao_nome,
            i.cnpj as instituicao_cnpj,
            i.selo_verificacao as instituicao_verificada,
            u.rua,
            u.numero,
            u.bairro,
            u.cidade,
            u.estado,
            u.cep,
            (SELECT COUNT(*) FROM apadrinha ap WHERE ap.id_animal = a.id_animal AND ap.status = 'Ativo') as padrinhos_ativos,
            (SELECT COUNT(*) FROM adota ad WHERE ad.id_animal = a.id_animal AND ad.status IN ('Aprovada', 'Aprovado')) as adocoes_aprovadas
        FROM animal a
        LEFT JOIN instituicao i ON a.id_instituicao = i.id_usuario
        LEFT JOIN usuario u ON i.id_usuario = u.id_usuario
        WHERE a.id_animal = $1;
    """

    query_prontuario = """
        SELECT 
            data_procedimento,
            tipo_procedimento,
            descricao
        FROM prontuario_veterinario
        WHERE id_animal = $1
        ORDER BY data_procedimento DESC;
    """

    query_telefones = """
        SELECT telefone FROM usuario_telefone WHERE id_usuario = $1;
    """

    async with pool.acquire() as conn:
        try:
            animal = await conn.fetchrow(query_animal, id_animal)
            if not animal:
                raise HTTPException(status_code=404, detail="Animal não encontrado.")

            prontuarios = await conn.fetch(query_prontuario, id_animal)
            telefones_raw = await conn.fetch(query_telefones, animal["id_instituicao"])
            telefones = [t["telefone"] for t in telefones_raw] if telefones_raw else []

            padrinhos = animal["padrinhos_ativos"]
            adocoes = animal["adocoes_aprovadas"]
            st_db = (animal["status_db"] or "").lower()
            if "adotado" in st_db or adocoes > 0:
                status_bloco = "Adotado"
            elif padrinhos > 0:
                status_bloco = "Ambos"
            else:
                status_bloco = "Adoção"

            fotos_especies = {
                "cão": "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=800&q=80",
                "gato": "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=800&q=80",
                "coelho": "https://images.unsplash.com/photo-1585110396000-c9ffd4e4b308?auto=format&fit=crop&w=800&q=80",
                "ave": "https://images.unsplash.com/photo-1522858547137-f1dcec554f55?auto=format&fit=crop&w=800&q=80",
                "papagaio": "https://images.unsplash.com/photo-1552728089-57bdde30beb3?auto=format&fit=crop&w=800&q=80",
                "calopsita": "https://images.unsplash.com/photo-1522858547137-f1dcec554f55?auto=format&fit=crop&w=800&q=80",
                "hamster": "https://images.unsplash.com/photo-1548767797-d8c844163c4c?auto=format&fit=crop&w=800&q=80",
                "porquinho-da-índia": "https://images.unsplash.com/photo-1548767797-d8c844163c4c?auto=format&fit=crop&w=800&q=80"
            }
            esp = (animal["especie"] or "").lower()
            foto_principal = fotos_especies.get(esp, "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=800&q=80")
            if "golden" in (animal["raca"] or "").lower():
                foto_principal = "https://images.unsplash.com/photo-1552053831-71594a27632d?auto=format&fit=crop&w=800&q=80"
            elif "siamês" in (animal["raca"] or "").lower():
                foto_principal = "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=800&q=80"
            elif "persa" in (animal["raca"] or "").lower():
                foto_principal = "https://images.unsplash.com/photo-1573865526739-10659fec78a5?auto=format&fit=crop&w=800&q=80"

            endereco_partes = [animal["rua"], animal["numero"], animal["bairro"], animal["cidade"], animal["estado"]]
            endereco_formatado = ", ".join([p for p in endereco_partes if p]) or "Não informado"

            return {
                "id_animal": animal["id_animal"],
                "nome": animal["nome"],
                "especie": animal["especie"],
                "raca": animal["raca"],
                "idade": f"{animal['idade']} ano(s)" if animal["idade"] else "Não informada",
                "porte": animal["porte"],
                "sexo": animal["sexo"],
                "status": status_bloco,
                "status_original": animal["status_db"],
                "observacao": animal["observacao"],
                "fotos": [
                    foto_principal,
                    "https://images.unsplash.com/photo-1517849845537-4d257902454a?auto=format&fit=crop&w=800&q=80",
                    "https://images.unsplash.com/photo-1537151625747-768eb6cf92b2?auto=format&fit=crop&w=800&q=80"
                ],
                "prontuario": [
                    {
                        "data": p["data_procedimento"].strftime("%d/%m/%Y"),
                        "procedimento": p["tipo_procedimento"],
                        "descricao": p["descricao"] or "Procedimento realizado com sucesso."
                    }
                    for p in prontuarios
                ],
                "instituicao": {
                    "id_usuario": animal["id_instituicao"],
                    "razao_social": animal["instituicao_nome"] or "Instituição Parceira",
                    "cnpj": animal["instituicao_cnpj"] or "Não informado",
                    "selo_verificacao": animal["instituicao_verificada"],
                    "endereco": endereco_formatado,
                    "telefone": telefones[0] if telefones else "Não informado"
                }
            }
        except HTTPException as h:
            raise h
        except Exception as e:
            print(f"Erro ao obter detalhes do animal: {e}")
            raise HTTPException(status_code=500, detail="Erro ao consultar detalhes do animal.")
