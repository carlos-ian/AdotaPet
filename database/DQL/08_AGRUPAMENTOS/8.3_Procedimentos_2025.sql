-- 8.3 Procedimentos de 2025 por tipo: quantidade, animais distintos, primeira e última data
SELECT pv.tipo_procedimento,
       COUNT(*) AS qtd_procedimentos,
       COUNT(DISTINCT pv.id_animal) AS animais_atendidos,
       MIN(pv.data_procedimento) AS primeira_data,
       MAX(pv.data_procedimento) AS ultima_data
FROM prontuario_veterinario pv
WHERE pv.data_procedimento BETWEEN '2025-01-01' AND '2025-12-31'
GROUP BY pv.tipo_procedimento;