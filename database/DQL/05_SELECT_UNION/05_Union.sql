-- Union de Animal com Inner Join de Adota/Apadrinha
SELECT 
    an.nome AS nome_pet,
    'Prontuário Médico' AS origem_nota,
    p.descricao AS detalhe_observacao
FROM Animal an
INNER JOIN Prontuario_Veterinario p ON an.id_animal = p.id_animal

UNION ALL

SELECT 
    an.nome AS nome_pet,
    'Processo de Adoção' AS origem_nota,
    ad.observacao_do_processo AS detalhe_observacao
FROM Animal an
INNER JOIN Adota ad ON an.id_animal = ad.id_animal;

-- Mostra histórico unificado de anotações e observações do Pet
-- com seu prontuário veterinario e acompanhamento de adoção