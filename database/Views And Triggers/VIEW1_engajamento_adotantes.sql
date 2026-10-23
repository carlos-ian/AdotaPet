CREATE OR REPLACE VIEW vw_engajamento_adotantes AS
-- Parte 1: Processos de Adoção Concluídos ou Em Análise
SELECT 
    ad.id_usuario AS id_adotante,
    ad.nome AS nome_adotante,
    an.nome AS nome_animal,
    an.especie,
    'Adoção' AS tipo_vinculo,
    a.status AS status_relacionamento,
    a.data_de_solicitacao AS data_registro
FROM adotante ad
INNER JOIN adota a ON ad.id_usuario = a.id_adotante
INNER JOIN animal an ON a.id_animal = an.id_animal

UNION

-- Parte 2: Apadrinhamentos Ativos
SELECT 
    ad.id_usuario AS id_adotante,
    ad.nome AS nome_adotante,
    an.nome AS nome_animal,
    an.especie,
    'Apadrinhamento' AS tipo_vinculo,
    ap.status AS status_relacionamento,
    ap.data_de_inicio AS data_registro
FROM adotante ad
INNER JOIN apadrinha ap ON ad.id_usuario = ap.id_adotante
INNER JOIN animal an ON ap.id_animal = an.id_animal;