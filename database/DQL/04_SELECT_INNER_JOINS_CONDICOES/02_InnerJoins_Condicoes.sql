-- Inner Joins com Adotante + Apadrinha + Animal + Instituição (4 Tabelas)
SELECT 
    a.nome AS nome_padrinho,
    an.nome AS nome_pet,
    i.razao_social AS ong_responsavel,
    ap.tipo_de_contribuicao,
    ap.valor_recorrente,
    ap.frequencia
FROM Adotante a
INNER JOIN Apadrinha ap ON a.id_usuario = ap.id_adotante
INNER JOIN Animal an ON ap.id_animal = an.id_animal
INNER JOIN Instituicao i ON an.id_instituicao = i.id_usuario
WHERE ap.status = 'Ativo' 
  AND ap.valor_recorrente >= 50.00;

-- Mostra apenas os apadrinhamentos ativos com valor recorrente maior ou igual a R$ 50,00 (condição)
-- trazendo informações do padrinho, animal apadrinhado e instituição responsável pelo animal