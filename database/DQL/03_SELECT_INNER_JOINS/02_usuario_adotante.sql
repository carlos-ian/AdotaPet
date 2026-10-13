-- Identificando dados completos dos adotantes cadastrados
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