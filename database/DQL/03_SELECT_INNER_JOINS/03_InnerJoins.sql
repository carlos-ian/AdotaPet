-- Inner Joins com Animal + Instituição (2 Tabelas)
SELECT 
    a.id_animal,
    a.nome AS nome_pet,
    a.especie,
	a.porte,
	a.idade,
    a.status AS status_pet,
    i.razao_social AS ong_responsavel
FROM Animal a
INNER JOIN Instituicao i ON a.id_instituicao = i.id_usuario;

-- Mostra todos os animais cadastrados e a instituição responsável por cada animal