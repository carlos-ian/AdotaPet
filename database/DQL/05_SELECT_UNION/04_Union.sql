-- Union de Usuario com Inner Join de Adota/Apadrinha
SELECT 
    a.id_usuario,
    a.nome AS nome_adotante,
    a.cpf,
    'Solicitou Adoção' AS tipo_engajamento
FROM Adotante a
INNER JOIN Adota ad ON a.id_usuario = ad.id_adotante

UNION

SELECT 
    a.id_usuario,
    a.nome AS nome_adotante,
    a.cpf,
    'Padrinho / Doador' AS tipo_engajamento
FROM Adotante a
INNER JOIN Apadrinha ap ON a.id_usuario = ap.id_adotante
WHERE ap.status = 'Ativo';

-- Mostra lista unificada de usuários do tipo adotante que solicitaram adoção ou 
-- são padrinhos/dadores ativos, com nome, CPF e tipo de engajamento.