-- Inner Joins com Adotante + Usuário (2 Tabelas)
SELECT 
    a.id_usuario,
    a.nome,
    a.cpf,
    a.tipo_residencia,
    u.email,
	u.senha,
    u.cidade,
	u.estado,
	u.bairro,
	u.cep
FROM Adotante a
INNER JOIN Usuario u ON a.id_usuario = u.id_usuario;

-- Mostra informações completas dos adotantes, informando dados específicos do adotante
-- e dados gerais do usuário, como email, senha, cidade, estado, bairro e cep