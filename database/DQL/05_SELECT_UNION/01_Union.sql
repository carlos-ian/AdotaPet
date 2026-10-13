-- Union com Adota + Apadrinha (2 Tabelas)
SELECT 
    ad.id_adotante,
    ad.id_animal,
    'Solicitação de Adoção' AS tipo_interacao,
    ad.status,
    ad.data_de_solicitacao AS data_registro
FROM Adota ad

UNION ALL

SELECT 
    ap.id_adotante,
    ap.id_animal,
    'Apadrinhamento Financeiro' AS tipo_interacao,
    ap.status,
    ap.data_de_inicio AS data_registro
FROM Apadrinha ap;

-- Mostra o histórico consolidado de adoções e apadrinhamentos com datas de inicio, status
-- identificação do animal e identificação do adotante