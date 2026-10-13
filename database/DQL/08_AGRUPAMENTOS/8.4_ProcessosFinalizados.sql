-- 8.4 Processos finalizados por status: quantidade e tempo médio de conclusão (dias)
SELECT ad.status,
       COUNT(*) AS qtd_processos,
       ROUND(AVG(ad.data_de_conclusao - ad.data_de_solicitacao), 1) AS media_dias_conclusao
FROM adota ad
WHERE ad.data_de_conclusao IS NOT NULL
GROUP BY ad.status;