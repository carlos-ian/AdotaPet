-- Inner Joins com Adotante + Adota + Animal (3 Tabelas)
SELECT 
    a.nome AS nome_adotante,
    a.tipo_residencia,
    an.nome AS nome_pet,
    an.especie,
    ad.status AS status_adocao,
    ad.data_de_solicitacao
FROM Adotante a
INNER JOIN Adota ad ON a.id_usuario = ad.id_adotante
INNER JOIN Animal an ON ad.id_animal = an.id_animal
WHERE ad.status != 'Recusado';

-- Mostra apenas os pedidos de adoção que não foram recusados (condição)
-- trazendo informações do adotante, tipo de residência, animal e status do pedido de adoção