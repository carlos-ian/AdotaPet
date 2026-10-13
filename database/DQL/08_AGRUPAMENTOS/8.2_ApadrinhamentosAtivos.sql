-- 8.2 Apadrinhamentos ATIVOS por padrinho: quantidade, soma, média e maior valor
SELECT ado.nome AS padrinho,
       COUNT(*) AS qtd_afilhados,
       SUM(ap.valor_recorrente) AS soma_valores,
       ROUND(AVG(ap.valor_recorrente), 2) AS valor_medio,
       MAX(ap.valor_recorrente) AS maior_valor
FROM apadrinha ap
JOIN adotante ado ON ado.id_usuario = ap.id_adotante
WHERE ap.status = 'Ativo'
GROUP BY ado.nome;