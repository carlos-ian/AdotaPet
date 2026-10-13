-- 9.4 Espécies com pelo menos 3 animais, por idade média
SELECT a.especie, COUNT(*) AS qtd_animais, ROUND(AVG(a.idade), 1) AS idade_media
FROM animal a
GROUP BY a.especie
HAVING COUNT(*) >= 3
ORDER BY idade_media DESC, a.especie ASC;