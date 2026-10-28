from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from backend.database import init_db, close_db, get_pool
from backend.schemas import (
    LoginSchema, RegistroSchema, AdocaoSchema, ApadrinhamentoSchema,
    PetSchema, StatusAdocaoSchema, StatusApadrinhamentoSchema,
    ProntuarioSchema, InstituicaoUpdateSchema
)

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

@app.get("/api/estatisticas")
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

@app.get("/api/pets/destaque")
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
                    pet["foto"] = "https://images.unsplash.com/photo-1543466835-00a7907e9de1?auto=format&fit=crop&q=80&w=600"
                pets_formatados.append(pet)
            return pets_formatados
        except Exception as e:
            print(f"Erro na consulta de pets em destaque: {e}")
            raise HTTPException(status_code=500, detail="Erro ao consultar o banco de dados")

@app.post("/api/login")
async def autenticar_usuario(dados: LoginSchema):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    query = """
        SELECT id_usuario, email, senha, tipo_usuario 
        FROM Usuario 
        WHERE LOWER(email) = LOWER($1);
    """

    async with pool.acquire() as conn:
        try:
            usuario = await conn.fetchrow(query, dados.email.strip())
            if not usuario:
                raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")

            if usuario["senha"] != dados.senha:
                raise HTTPException(status_code=401, detail="E-mail ou senha incorretos.")

            tipo_bd = usuario["tipo_usuario"].strip().lower()
            tipo_envio = dados.tipo_usuario.strip().lower()

            is_bd_inst = tipo_bd in ["instituicao", "instituição", "ong"]
            is_envio_inst = tipo_envio in ["instituicao", "instituição", "ong"]

            if is_bd_inst != is_envio_inst:
                perfil_correto = "Instituição" if is_bd_inst else "Adotante"
                raise HTTPException(
                    status_code=403, 
                    detail=f"Perfil incorreto! Sua conta está cadastrada como '{perfil_correto}'. Por favor, altere o perfil acima para entrar."
                )

            if is_bd_inst:
                inst = await conn.fetchrow("SELECT razao_social FROM Instituicao WHERE id_usuario = $1", usuario["id_usuario"])
                nome_display = inst["razao_social"] if inst and inst["razao_social"] else "Instituição"
                redirect_page = "dashboard-instituicao.html"
            else:
                adot = await conn.fetchrow("SELECT nome FROM Adotante WHERE id_usuario = $1", usuario["id_usuario"])
                nome_display = adot["nome"] if adot and adot["nome"] else "Adotante"
                redirect_page = "dashboard-adotante.html"

            return {
                "mensagem": "Login realizado com sucesso!",
                "usuario": {
                    "id_usuario": usuario["id_usuario"],
                    "email": usuario["email"],
                    "tipo_usuario": usuario["tipo_usuario"],
                    "nome": nome_display
                },
                "redirect": redirect_page
            }
        except HTTPException as http_err:
            raise http_err
        except Exception as e:
            print(f"Erro no processamento de login: {e}")
            raise HTTPException(status_code=500, detail="Erro interno durante a autenticação.")

@app.post("/api/registrar")
async def registrar_usuario(dados: RegistroSchema):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    async with pool.acquire() as conn:
        async with conn.transaction():
            try:
                usuario_existente = await conn.fetchval("SELECT id_usuario FROM Usuario WHERE LOWER(email) = LOWER($1)", dados.email.strip())
                if usuario_existente:
                    raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado no sistema.")

                query_usuario = """
                    INSERT INTO Usuario (email, senha, rua, numero, bairro, cep, cidade, estado, complemento, tipo_usuario)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                    RETURNING id_usuario;
                """
                id_usuario = await conn.fetchval(
                    query_usuario,
                    dados.email.strip(),
                    dados.senha,
                    dados.rua,
                    dados.numero,
                    dados.bairro,
                    dados.cep,
                    dados.cidade,
                    dados.estado,
                    dados.complemento,
                    dados.tipo_usuario
                )

                if dados.tipo_usuario.lower() == "adotante":
                    if not dados.nome or not dados.cpf:
                        raise HTTPException(status_code=400, detail="Nome e CPF são obrigatórios para Adotantes.")
                    cpf_limpo = dados.cpf.replace(".", "").replace("-", "").strip()
                    query_adotante = """
                        INSERT INTO Adotante (id_usuario, nome, cpf, tipo_residencia)
                        VALUES ($1, $2, $3, $4);
                    """
                    await conn.execute(query_adotante, id_usuario, dados.nome.strip(), cpf_limpo, dados.tipo_residencia)

                elif dados.tipo_usuario.lower() in ["instituicao", "instituição", "ong"]:
                    if not dados.razao_social or not dados.cnpj:
                        raise HTTPException(status_code=400, detail="Razão Social e CNPJ são obrigatórios para Instituições.")
                    cnpj_limpo = dados.cnpj.replace(".", "").replace("/", "").replace("-", "").strip()
                    query_instituicao = """
                        INSERT INTO Instituicao (id_usuario, razao_social, cnpj, selo_verificacao)
                        VALUES ($1, $2, $3, $4);
                    """
                    await conn.execute(query_instituicao, id_usuario, dados.razao_social.strip(), cnpj_limpo, False)

                if dados.telefones:
                    query_telefone = "INSERT INTO usuario_telefone (id_usuario, telefone) VALUES ($1, $2);"
                    for tel in dados.telefones:
                        if tel and tel.strip():
                            await conn.execute(query_telefone, id_usuario, tel.strip())

                return {"mensagem": "Conta criada com sucesso!", "id_usuario": id_usuario}
            except HTTPException as http_err:
                raise http_err
            except Exception as e:
                print(f"Erro ao registrar usuário: {e}")
                raise HTTPException(status_code=500, detail="Erro interno ao gravar dados do usuário.")

@app.get("/api/dashboard/estatisticas-brasil")
async def obter_estatisticas_brasil():
    return {
        "animaisSobTutela": "+185 mil",
        "taxaSucesso": "94%",
        "prontuariosAuditados": "100%"
    }

@app.get("/api/animais")
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

@app.get("/api/animais/{id_animal}")
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

@app.get("/api/instituicoes")
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

@app.get("/api/instituicoes/{id_instituicao}")
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

@app.get("/api/adotante/{id_usuario}")
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

@app.get("/api/adotante/{id_usuario}/adocoes")
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

@app.get("/api/adotante/{id_usuario}/apadrinhamentos")
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

@app.post("/api/adocao")
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

@app.post("/api/apadrinhamento")
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

@app.get("/api/instituicao/{id_instituicao}/dashboard")
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

@app.post("/api/instituicao/pets")
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

# ROTA ÚNICA E CORRIGIDA PARA ATUALIZAR STATUS DA ADOÇÃO
@app.put("/api/instituicao/adocoes/status")
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

@app.put("/api/instituicao/pets/{id_animal}")
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

@app.delete("/api/instituicao/pets/{id_animal}")
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

@app.get("/api/instituicao/{id_instituicao}/adocoes")
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

@app.get("/api/instituicao/{id_instituicao}/apadrinhamentos")
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

@app.put("/api/instituicao/apadrinhamentos/status")
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

@app.get("/api/prontuario/{id_animal}")
async def obter_prontuario_animal(id_animal: int):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    query_animal = "SELECT id_animal, nome, especie, raca, id_instituicao FROM animal WHERE id_animal = $1;"
    query_pront = """
        SELECT id_prontuario, data_procedimento, tipo_procedimento, descricao
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
                        "id_prontuario": r["id_prontuario"],
                        "data": r["data_procedimento"].strftime("%d/%m/%Y") if r["data_procedimento"] else "-",
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

@app.post("/api/prontuario")
async def criar_registro_prontuario(dados: ProntuarioSchema):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    query = """
        INSERT INTO prontuario_veterinario (id_animal, data_procedimento, tipo_procedimento, descricao)
        VALUES ($1, CURRENT_DATE, $2, $3)
        RETURNING id_prontuario;
    """
    async with pool.acquire() as conn:
        try:
            id_p = await conn.fetchval(query, dados.id_animal, dados.tipo_procedimento, dados.descricao)
            return {"mensagem": "Registro adicionado ao prontuário!", "id_prontuario": id_p}
        except Exception as e:
            print(f"Erro ao adicionar prontuário: {e}")
            raise HTTPException(status_code=500, detail="Erro ao gravar ficha clínica.")

@app.get("/api/instituicao/{id_instituicao}/perfil")
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

@app.put("/api/instituicao/{id_instituicao}/perfil")
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

@app.delete("/api/instituicao/{id_instituicao}")
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