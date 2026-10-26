from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from database import init_db, close_db, get_pool
from schemas import LoginSchema, RegistroSchema

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

# Get de Dados Gerais para Tela Home
@app.get("/api/estatisticas")
async def obter_estatisticas():
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    async with pool.acquire() as conn:
        try:
            total_resgatados = await conn.fetchval("SELECT COUNT(*) FROM Animal")
            
            total_adocoes = await conn.fetchval("SELECT COUNT(*) FROM Adota WHERE status = 'Aprovada' OR status = 'Concluída'")
            
            total_padrinhos = await conn.fetchval("SELECT COUNT(*) FROM Apadrinha WHERE status = 'Ativo'")
            
            query_ongs = """
                SELECT 
                    ROUND((COUNT(CASE WHEN selo_verificacao = TRUE THEN 1 END) * 100.0) / NULLIF(COUNT(*), 0))
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

# Get para obter Pets para Tela Home
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

# Post para autenticação de usuário (Login)
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
                inst = await conn.fetchrow(
                    "SELECT razao_social FROM Instituicao WHERE id_usuario = $1", 
                    usuario["id_usuario"]
                )
                nome_display = inst["razao_social"] if inst and inst["razao_social"] else "Instituição"
                redirect_page = "dashboard-instituicao.html"
            else:
                adot = await conn.fetchrow(
                    "SELECT nome FROM Adotante WHERE id_usuario = $1", 
                    usuario["id_usuario"]
                )
                nome_display = adot["nome"] if adot and adot["nome"] else "Adotante"
                redirect_page = "painel-adotante.html"

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

# Post para registrar novo usuário (Registro)
@app.post("/api/registrar")
async def registrar_usuario(dados: RegistroSchema):
    pool = get_pool()
    if not pool:
        raise HTTPException(status_code=500, detail="Banco de dados não conectado")

    async with pool.acquire() as conn:
        # Abre transação atômica
        async with conn.transaction():
            try:
                usuario_existente = await conn.fetchval("SELECT id_usuario FROM Usuario WHERE email = $1", dados.email)
                if usuario_existente:
                    raise HTTPException(status_code=400, detail="Este e-mail já está cadastrado no sistema.")

                query_usuario = """
                    INSERT INTO Usuario (email, senha, rua, numero, bairro, cep, cidade, estado, complemento, tipo_usuario)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                    RETURNING id_usuario;
                """
                id_usuario = await conn.fetchval(
                    query_usuario,
                    dados.email,
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
                    await conn.execute(
                        query_adotante,
                        id_usuario,
                        dados.nome.strip(),
                        cpf_limpo,
                        dados.tipo_residencia
                    )

                elif dados.tipo_usuario.lower() in ["instituicao", "instituição", "ong"]:
                    if not dados.razao_social or not dados.cnpj:
                        raise HTTPException(status_code=400, detail="Razão Social e CNPJ são obrigatórios para Instituições.")

                    query_instituicao = """
                        INSERT INTO Instituicao (id_usuario, razao_social, cnpj, selo_verificacao)
                        VALUES ($1, $2, $3, $4);
                    """
                    await conn.execute(
                        query_instituicao,
                        id_usuario,
                        dados.razao_social,
                        dados.cnpj,
                        False
                    )

                if dados.telefones:
                    query_telefone = """
                        INSERT INTO usuario_telefone (id_usuario, telefone)
                        VALUES ($1, $2);
                    """
                    for tel in dados.telefones:
                        if tel.strip():
                            await conn.execute(query_telefone, id_usuario, tel.strip())

                return {"mensagem": "Conta criada com sucesso!", "id_usuario": id_usuario}

            except HTTPException as http_err:
                raise http_err
            except Exception as e:
                print(f"Erro ao registrar usuário: {e}")
                raise HTTPException(status_code=500, detail="Erro interno ao gravar dados do usuário.")