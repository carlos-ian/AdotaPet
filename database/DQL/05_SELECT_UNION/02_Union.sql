-- Union com Adotante + Instituição (2 Tabelas) e Inner Join com Usuário (1 Tabela)
SELECT 
    a.nome AS nome_razao,
    a.cpf AS documento,
    'Pessoa Física (CPF)' AS tipo_documento,
    u.cidade,
    u.estado
FROM Adotante a
INNER JOIN Usuario u ON a.id_usuario = u.id_usuario

UNION

SELECT 
    i.razao_social AS nome_razao,
    i.cnpj AS documento,
    'Pessoa Jurídica (CNPJ)' AS tipo_documento,
    u.cidade,
    u.estado
FROM Instituicao i
INNER JOIN Usuario u ON u.id_usuario = i.id_usuario;

-- Mostra lista unificada de usuários do tipo adotante e instituição, com nome/razão social, 
-- documento (CPF/CNPJ), tipo de documento, cidade e estado.