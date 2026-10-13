-- Inner Joins com Adotante + Adota + Animal + Instituição (4 Tabelas)
SELECT 
    an.nome AS nome_pet,
    an.especie,
    an.porte,
    i.razao_social AS ong_responsavel,
    a.nome AS nome_adotante,
    a.tipo_residencia,
    ad.status AS status_adocao
FROM Animal an
INNER JOIN Instituicao i ON an.id_instituicao = i.id_usuario
INNER JOIN Adota ad ON an.id_animal = ad.id_animal
INNER JOIN Adotante a ON ad.id_adotante = a.id_usuario
WHERE ad.status IN ('Em Análise')
  AND LOWER(a.tipo_residencia) LIKE '%apartamento%';

-- Mostra apenas os animais em processo de adoção cujos adotantes moram em apartamento (condição)
-- trazendo informações do animal, ONG responsável e adotante