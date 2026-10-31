from fastapi import APIRouter, HTTPException
from backend.database import get_pool
from backend.schemas import LoginSchema, RegistroSchema

router = APIRouter(prefix="/api", tags=["Autenticação"])

@router.post("/login")
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

@router.post("/registrar")
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
