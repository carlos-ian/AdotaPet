from fastapi import APIRouter, HTTPException
from backend.database import get_pool
from backend.schemas import PetSchema, StatusAdocaoSchema, StatusApadrinhamentoSchema, InstituicaoUpdateSchema

router = APIRouter(prefix="/api", tags=["Instituições"])

@router.get("/instituicoes")
async def listar_instituicoes(busca: str = None, cidade: str = None, estado: str = None):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    query = """
        SELECT 
            i.id_usuario,
            i.cnpj,
            i.razao_social,
            i.selo_verificacao,
            u.email,
            u.rua,
            u.numero,
            u.bairro,
            u.cidade,
            u.estado,
            u.cep,
            (SELECT COUNT(*) FROM animal a WHERE a.id_instituicao = i.id_usuario) as total_animais,
            (SELECT COUNT(*) FROM animal a WHERE a.id_instituicao = i.id_usuario AND a.status = 'Disponível') as animais_disponiveis
        FROM instituicao i
        JOIN usuario u ON i.id_usuario = u.id_usuario
        ORDER BY i.razao_social;
    """

    async with pool.acquire() as conn:
        try:
            rows = await conn.fetch(query)
            resultado = []
            for r in rows:
                tels_raw = await conn.fetch("SELECT telefone FROM usuario_telefone WHERE id_usuario = $1", r["id_usuario"])
                tels = [t["telefone"] for t in tels_raw] if tels_raw else []

                item = {
                    "id_usuario": r["id_usuario"],
                    "razao_social": r["razao_social"],
                    "cnpj": r["cnpj"],
                    "selo_verificacao": r["selo_verificacao"],
                    "email": r["email"],
                    "rua": r["rua"],
                    "numero": r["numero"],
                    "bairro": r["bairro"],
                    "cidade": r["cidade"],
                    "estado": r["estado"],
                    "cep": r["cep"],
                    "telefones": tels,
                    "total_animais": r["total_animais"],
                    "animais_disponiveis": r["animais_disponiveis"]
                }

                if busca:
                    b = busca.lower()
                    if not (b in (item["razao_social"] or "").lower() or b in (item["cidade"] or "").lower() or b in (item["cnpj"] or "").lower()):
                        continue
                if cidade and (item["cidade"] or "").lower() != cidade.lower():
                    continue
                if estado and (item["estado"] or "").upper() != estado.upper():
                    continue

                resultado.append(item)
            return resultado
        except Exception as e:
            print(f"Erro ao listar instituições: {e}")
            raise HTTPException(status_code=500, detail="Erro ao consultar instituições.")

@router.get("/instituicoes/{id_instituicao}")
async def obter_detalhes_instituicao(id_instituicao: int):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    query_inst = """
        SELECT 
            i.id_usuario,
            i.cnpj,
            i.razao_social,
            i.selo_verificacao,
            u.email,
            u.rua,
            u.numero,
            u.bairro,
            u.cidade,
            u.estado,
            u.cep,
            u.complemento
        FROM instituicao i
        JOIN usuario u ON i.id_usuario = u.id_usuario
        WHERE i.id_usuario = $1;
    """

    query_telefones = """
        SELECT telefone FROM usuario_telefone WHERE id_usuario = $1;
    """

    query_pets = """
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
            (SELECT COUNT(*) FROM apadrinha ap WHERE ap.id_animal = a.id_animal AND ap.status = 'Ativo') as padrinhos_ativos,
            (SELECT COUNT(*) FROM adota ad WHERE ad.id_animal = a.id_animal AND ad.status IN ('Aprovada', 'Aprovado')) as adocoes_aprovadas
        FROM animal a
        WHERE a.id_instituicao = $1
        ORDER BY a.id_animal;
    """

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

    async with pool.acquire() as conn:
        try:
            inst = await conn.fetchrow(query_inst, id_instituicao)
            if not inst:
                raise HTTPException(status_code=404, detail="Instituição não encontrada.")

            telefones_raw = await conn.fetch(query_telefones, id_instituicao)
            telefones = [t["telefone"] for t in telefones_raw] if telefones_raw else []

            pets_raw = await conn.fetch(query_pets, id_instituicao)
            pets = []
            for p in pets_raw:
                padrinhos = p["padrinhos_ativos"]
                adocoes = p["adocoes_aprovadas"]
                st_db = (p["status_db"] or "").lower()
                if "adotado" in st_db or adocoes > 0:
                    status_bloco = "Adotado"
                elif padrinhos > 0:
                    status_bloco = "Ambos"
                else:
                    status_bloco = "Adoção"

                esp = (p["especie"] or "").lower()
                foto_url = fotos_especies.get(esp, "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&w=600&q=80")
                if "golden" in (p["raca"] or "").lower():
                    foto_url = "https://images.unsplash.com/photo-1552053831-71594a27632d?auto=format&fit=crop&w=600&q=80"
                elif "siamês" in (p["raca"] or "").lower():
                    foto_url = "https://images.unsplash.com/photo-1514888286974-6c03e2ca1dba?auto=format&fit=crop&w=600&q=80"
                elif "persa" in (p["raca"] or "").lower():
                    foto_url = "https://images.unsplash.com/photo-1573865526739-10659fec78a5?auto=format&fit=crop&w=600&q=80"

                pets.append({
                    "id_animal": p["id_animal"],
                    "nome": p["nome"],
                    "especie": p["especie"],
                    "raca": p["raca"],
                    "idade": f"{p['idade']} ano(s)" if p["idade"] else "Não informada",
                    "porte": p["porte"],
                    "sexo": p["sexo"],
                    "status": status_bloco,
                    "observacao": p["observacao"],
                    "foto": foto_url
                })

            endereco_partes = [inst["rua"], inst["numero"], inst["complemento"], inst["bairro"], inst["cidade"], inst["estado"], inst["cep"]]
            endereco_formatado = ", ".join([p for p in endereco_partes if p]) or "Não informado"

            return {
                "id_usuario": inst["id_usuario"],
                "razao_social": inst["razao_social"],
                "cnpj": inst["cnpj"],
                "selo_verificacao": inst["selo_verificacao"],
                "email": inst["email"],
                "endereco": endereco_formatado,
                "cidade": inst["cidade"],
                "estado": inst["estado"],
                "telefones": telefones,
                "pets": pets,
                "total_pets": len(pets)
            }
        except HTTPException as h:
            raise h
        except Exception as e:
            print(f"Erro ao obter detalhes da instituição: {e}")
            raise HTTPException(status_code=500, detail="Erro ao consultar detalhes da instituição.")

@router.get("/instituicao/{id_instituicao}/dashboard")
async def obter_dashboard_instituicao(id_instituicao: int):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    async with pool.acquire() as conn:
        try:
            total_pets = await conn.fetchval("SELECT COUNT(*) FROM animal WHERE id_instituicao = $1", id_instituicao) or 0
            
            adocoes_pendentes = await conn.fetchval("""
                SELECT COUNT(*) FROM adota ad
                JOIN animal a ON ad.id_animal = a.id_animal
                WHERE a.id_instituicao = $1 AND ad.status IN ('Em Análise', 'Solicitada')
            """, id_instituicao) or 0

            padrinhos_ativos = await conn.fetchval("""
                SELECT COUNT(*) FROM apadrinha ap
                JOIN animal a ON ap.id_animal = a.id_animal
                WHERE a.id_instituicao = $1 AND ap.status = 'Ativo'
            """, id_instituicao) or 0

            prontuarios_mes = await conn.fetchval("""
                SELECT COUNT(*) FROM prontuario_veterinario pv
                JOIN animal a ON pv.id_animal = a.id_animal
                WHERE a.id_instituicao = $1 AND pv.data_procedimento >= date_trunc('month', CURRENT_DATE)
            """, id_instituicao) or 0

            ultimas_adocoes = await conn.fetch("""
                SELECT 
                    a.id_animal,
                    a.nome as pet_nome,
                    a.especie as pet_especie,
                    ad.id_adotante,
                    adot.nome as adotante_nome,
                    ad.data_de_solicitacao,
                    ad.status
                FROM adota ad
                JOIN animal a ON ad.id_animal = a.id_animal
                JOIN adotante adot ON ad.id_adotante = adot.id_usuario
                WHERE a.id_instituicao = $1
                ORDER BY ad.data_de_solicitacao DESC LIMIT 5
            """, id_instituicao)

            procedimentos = await conn.fetch("""
                SELECT 
                    pv.id_animal,
                    a.nome as pet_nome,
                    pv.tipo_procedimento,
                    pv.descricao,
                    pv.data_procedimento
                FROM prontuario_veterinario pv
                JOIN animal a ON pv.id_animal = a.id_animal
                WHERE a.id_instituicao = $1
                ORDER BY pv.data_procedimento DESC LIMIT 5
            """, id_instituicao)

            return {
                "metricas": {
                    "totalPets": total_pets,
                    "adocoesPendentes": adocoes_pendentes,
                    "padrinhosAtivos": padrinhos_ativos,
                    "prontuariosMes": prontuarios_mes
                },
                "ultimasAdocoes": [
                    {
                        "id_animal": r["id_animal"],
                        "id_adotante": r["id_adotante"],
                        "pet_nome": r["pet_nome"],
                        "pet_especie": r["pet_especie"],
                        "adotante_nome": r["adotante_nome"],
                        "data": r["data_de_solicitacao"].strftime("%d/%m/%Y") if r["data_de_solicitacao"] else "-",
                        "status": r["status"]
                    } for r in ultimas_adocoes
                ],
                "procedimentos": [
                    {
                        "id_animal": r["id_animal"],
                        "pet_nome": r["pet_nome"],
                        "tipo": r["tipo_procedimento"],
                        "descricao": r["descricao"] or "Procedimento registrado.",
                        "data": r["data_procedimento"].strftime("%d/%m/%Y") if r["data_procedimento"] else "-"
                    } for r in procedimentos
                ]
            }
        except Exception as e:
            print(f"Erro no dashboard da instituição: {e}")
            raise HTTPException(status_code=500, detail="Erro ao carregar dados do dashboard.")

@router.post("/instituicao/pets")
async def criar_pet(dados: PetSchema):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    query = """
        INSERT INTO animal (nome, especie, raca, idade, porte, sexo, status, observacao, id_instituicao)
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
        RETURNING id_animal;
    """
    async with pool.acquire() as conn:
        try:
            raca_val = dados.raca.strip() if dados.raca else "SRD"
            obs_val = dados.observacao.strip() if dados.observacao else ""
            idade_val = dados.idade if dados.idade is not None else 0

            sexo_val = dados.sexo.strip()[0].upper() if dados.sexo else "M"
            porte_val = dados.porte.strip()[0].upper() if dados.porte else "M"

            id_pet = await conn.fetchval(
                query,
                dados.nome.strip(),
                dados.especie.strip(),
                raca_val,
                idade_val,
                porte_val,
                sexo_val,
                dados.status,
                obs_val,
                dados.id_instituicao
            )
            return {"mensagem": "Pet cadastrado com sucesso!", "id_animal": id_pet}
        except Exception as e:
            print(f"❌ Erro ao criar pet: {e}")
            raise HTTPException(status_code=500, detail=f"Erro ao cadastrar novo pet: {str(e)}")

@router.put("/instituicao/pets/{id_animal}")
async def atualizar_pet(id_animal: int, dados: PetSchema):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    query = """
        UPDATE animal
        SET nome = $1, especie = $2, raca = $3, idade = $4, porte = $5, sexo = $6, status = $7, observacao = $8
        WHERE id_animal = $9 AND id_instituicao = $10;
    """
    async with pool.acquire() as conn:
        try:
            sexo_val = dados.sexo.strip()[0].upper() if dados.sexo else "M"
            porte_val = dados.porte.strip()[0].upper() if dados.porte else "M"

            await conn.execute(
                query,
                dados.nome.strip(),
                dados.especie.strip(),
                dados.raca,
                dados.idade,
                porte_val,
                sexo_val,
                dados.status,
                dados.observacao,
                id_animal,
                dados.id_instituicao
            )
            return {"mensagem": "Pet atualizado com sucesso!"}
        except Exception as e:
            print(f"Erro ao atualizar pet: {e}")
            raise HTTPException(status_code=500, detail="Erro ao atualizar pet.")

@router.delete("/instituicao/pets/{id_animal}")
async def excluir_pet(id_animal: int, id_instituicao: int):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    async with pool.acquire() as conn:
        try:
            await conn.execute("DELETE FROM animal WHERE id_animal = $1 AND id_instituicao = $2", id_animal, id_instituicao)
            return {"mensagem": "Pet removido do sistema."}
        except Exception as e:
            print(f"Erro ao excluir pet: {e}")
            raise HTTPException(status_code=500, detail="Erro ao remover pet.")

@router.put("/instituicao/adocoes/status")
async def atualizar_status_adocao(dados: StatusAdocaoSchema):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    status_val = str(dados.status).strip().replace("'", "''")
    obs_val = str(dados.observacao or "").strip().replace("'", "''")
    id_adotante = int(dados.id_adotante)
    id_animal = int(dados.id_animal)

    sql_adota = f"""
        UPDATE adota
        SET status = '{status_val}'::character varying, 
            observacao_do_processo = '{obs_val}'::text
        WHERE id_adotante = {id_adotante} AND id_animal = {id_animal};
    """

    async with pool.acquire() as conn:
        try:
            await conn.execute(sql_adota)

            if status_val in ["Aprovada", "Aprovado", "Concluída"]:
                sql_animal = f"""
                    UPDATE animal 
                    SET status = 'Adotado'::character varying 
                    WHERE id_animal = {id_animal};
                """
                await conn.execute(sql_animal)

            return {"mensagem": "Status da adoção atualizado com sucesso!"}
        except Exception as e:
            print(f"❌ Erro ao atualizar adoção: {e}")
            raise HTTPException(status_code=500, detail=f"Erro ao atualizar processo de adoção: {str(e)}")

@router.get("/instituicao/{id_instituicao}/adocoes")
async def listar_adocoes_instituicao(id_instituicao: int):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    query = """
        SELECT 
            a.id_adotante,
            a.id_animal,
            a.status,
            a.observacao_do_processo,
            an.nome AS nome_animal,
            u.email AS email_adotante
        FROM adota a
        JOIN animal an ON a.id_animal = an.id_animal
        JOIN usuario u ON a.id_adotante = u.id_usuario
        WHERE an.id_instituicao = $1;
    """
    async with pool.acquire() as conn:
        try:
            rows = await conn.fetch(query, id_instituicao)
            resultado = []
            for r in rows:
                item = dict(r)
                item['nome_adotante'] = item['email_adotante']
                item['data_de_inicio'] = None
                resultado.append(item)
            return resultado
        except Exception as e:
            print(f"❌ Erro ao listar adoções: {e}")
            raise HTTPException(status_code=500, detail=str(e))

@router.get("/instituicao/{id_instituicao}/apadrinhamentos")
async def listar_apadrinhamentos_instituicao(id_instituicao: int):
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
            adot.nome as padrinho_nome,
            u.email as padrinho_email
        FROM apadrinha ap
        JOIN animal a ON ap.id_animal = a.id_animal
        JOIN adotante adot ON ap.id_adotante = adot.id_usuario
        JOIN usuario u ON adot.id_usuario = u.id_usuario
        WHERE a.id_instituicao = $1
        ORDER BY ap.data_de_inicio DESC;
    """
    async with pool.acquire() as conn:
        try:
            rows = await conn.fetch(query, id_instituicao)
            return [
                {
                    "id_adotante": r["id_adotante"],
                    "id_animal": r["id_animal"],
                    "pet_nome": r["pet_nome"],
                    "pet_especie": r["pet_especie"],
                    "padrinho_nome": r["padrinho_nome"],
                    "padrinho_email": r["padrinho_email"],
                    "tipo_de_contribuicao": r["tipo_de_contribuicao"],
                    "valor_recorrente": float(r["valor_recorrente"]) if r["valor_recorrente"] is not None else 0.0,
                    "frequencia": r["frequencia"],
                    "status": r["status"],
                    "data_inicio": r["data_de_inicio"].strftime("%d/%m/%Y") if r["data_de_inicio"] else "-"
                } for r in rows
            ]
        except Exception as e:
            print(f"Erro ao listar apadrinhamentos: {e}")
            raise HTTPException(status_code=500, detail="Erro ao consultar apadrinhamentos.")

@router.put("/instituicao/apadrinhamentos/status")
async def atualizar_status_apadrinhamento(dados: StatusApadrinhamentoSchema):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    query = "UPDATE apadrinha SET status = $1 WHERE id_adotante = $2 AND id_animal = $3;"
    async with pool.acquire() as conn:
        try:
            await conn.execute(query, dados.status, dados.id_adotante, dados.id_animal)
            return {"mensagem": "Status do apadrinhamento alterado!"}
        except Exception as e:
            print(f"Erro ao atualizar apadrinhamento: {e}")
            raise HTTPException(status_code=500, detail="Erro ao alterar status.")

@router.get("/instituicao/{id_instituicao}/perfil")
async def obter_perfil_instituicao_dados(id_instituicao: int):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    query = """
        SELECT 
            i.id_usuario, i.razao_social, i.cnpj, i.selo_verificacao,
            u.email, u.rua, u.numero, u.bairro, u.cidade, u.estado, u.cep, u.complemento
        FROM instituicao i
        JOIN usuario u ON i.id_usuario = u.id_usuario
        WHERE i.id_usuario = $1;
    """
    async with pool.acquire() as conn:
        try:
            inst = await conn.fetchrow(query, id_instituicao)
            if not inst:
                raise HTTPException(status_code=404, detail="Instituição não encontrada.")
            tels_raw = await conn.fetch("SELECT telefone FROM usuario_telefone WHERE id_usuario = $1", id_instituicao)
            tels = [t["telefone"] for t in tels_raw] if tels_raw else []
            res = dict(inst)
            res["telefones"] = tels
            return res
        except HTTPException as h:
            raise h
        except Exception as e:
            print(f"Erro ao obter perfil da instituição: {e}")
            raise HTTPException(status_code=500, detail="Erro ao carregar perfil.")

@router.put("/instituicao/{id_instituicao}/perfil")
async def atualizar_perfil_instituicao(id_instituicao: int, dados: InstituicaoUpdateSchema):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    async with pool.acquire() as conn:
        async with conn.transaction():
            try:
                await conn.execute("""
                    UPDATE usuario
                    SET email = $1, rua = $2, numero = $3, bairro = $4, cidade = $5, estado = $6, cep = $7, complemento = $8
                    WHERE id_usuario = $9;
                """, dados.email, dados.rua, dados.numero, dados.bairro, dados.cidade, dados.estado, dados.cep, dados.complemento, id_instituicao)

                cnpj_limpo = dados.cnpj.replace(".", "").replace("/", "").replace("-", "").strip()
                await conn.execute("""
                    UPDATE instituicao
                    SET razao_social = $1, cnpj = $2
                    WHERE id_usuario = $3;
                """, dados.razao_social, cnpj_limpo, id_instituicao)

                await conn.execute("DELETE FROM usuario_telefone WHERE id_usuario = $1;", id_instituicao)
                if dados.telefones:
                    for tel in dados.telefones:
                        if tel and tel.strip():
                            await conn.execute("INSERT INTO usuario_telefone (id_usuario, telefone) VALUES ($1, $2);", id_instituicao, tel.strip())

                return {"mensagem": "Dados da instituição atualizados com sucesso!"}
            except Exception as e:
                print(f"Erro ao atualizar perfil da instituição: {e}")
                raise HTTPException(status_code=500, detail="Erro ao salvar dados.")

@router.delete("/instituicao/{id_instituicao}")
async def apagar_conta_instituicao(id_instituicao: int):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    async with pool.acquire() as conn:
        async with conn.transaction():
            try:
                await conn.execute("DELETE FROM usuario_telefone WHERE id_usuario = $1;", id_instituicao)
                pets = await conn.fetch("SELECT id_animal FROM animal WHERE id_instituicao = $1;", id_instituicao)
                for p in pets:
                    pid = p["id_animal"]
                    await conn.execute("DELETE FROM prontuario_veterinario WHERE id_animal = $1;", pid)
                    await conn.execute("DELETE FROM adota WHERE id_animal = $1;", pid)
                    await conn.execute("DELETE FROM apadrinha WHERE id_animal = $1;", pid)
                await conn.execute("DELETE FROM animal WHERE id_instituicao = $1;", id_instituicao)
                await conn.execute("DELETE FROM instituicao WHERE id_usuario = $1;", id_instituicao)
                await conn.execute("DELETE FROM usuario WHERE id_usuario = $1;", id_instituicao)
                return {"mensagem": "Conta e todos os dados associados foram removidos com sucesso."}
            except Exception as e:
                print(f"Erro ao apagar conta da instituição: {e}")
                raise HTTPException(status_code=500, detail="Erro ao deletar conta.")
