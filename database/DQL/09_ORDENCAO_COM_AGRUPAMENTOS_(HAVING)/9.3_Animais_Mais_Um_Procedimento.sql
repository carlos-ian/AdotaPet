-- 9.3 Animais com mais de um procedimento veterinário
SELECT a.nome AS animal, a.especie,
       COUNT(*) AS qtd_procedimentos,
       MAX(pv.data_procedimento) AS ultimo_procedimento
FROM prontuario_veterinario pv
JOIN animal a ON a.id_animal = pv.id_animal
GROUP BY a.id_animal, a.nome, a.especie
HAVING COUNT(*) > 1
ORDER BY qtd_procedimentos DESC, ultimo_procedimento DESC;