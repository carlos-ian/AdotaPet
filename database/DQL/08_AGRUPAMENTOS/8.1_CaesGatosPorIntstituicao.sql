-- 8.1 Cães e gatos por instituição: total, disponíveis, idade média/mín/máx
SELECT i.razao_social AS instituicao,
       COUNT(*) AS total_caes_gatos,
       COUNT(*) FILTER (WHERE a.status = 'Disponível') AS disponiveis,
       ROUND(AVG(a.idade), 1) AS idade_media,
       MIN(a.idade) AS idade_min,
       MAX(a.idade) AS idade_max
FROM animal a
JOIN instituicao i ON i.id_usuario = a.id_instituicao
WHERE a.especie IN ('Cão', 'Gato')
GROUP BY i.razao_social;