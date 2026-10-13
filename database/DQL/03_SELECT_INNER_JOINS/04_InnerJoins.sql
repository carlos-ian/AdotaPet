-- Inner Joins com Usuário + Adotante + Adotante_Historico_Pets (3 Tabelas)
SELECT 
    u.email,
    a.nome AS nome_adotante,
	a.cpf,
	hp.descricao
FROM Usuario u
INNER JOIN Adotante a ON u.id_usuario = a.id_usuario
INNER JOIN Adotante_Historico_Pets hp ON a.id_usuario = hp.id_usuario;

-- Mostra informações dos adotantes gerais e específicas com seu histórico de pets