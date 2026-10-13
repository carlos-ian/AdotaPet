-- 9.1 Instituições com 5 ou mais animais disponíveis
SELECT i.razao_social AS instituicao, COUNT(*) AS animais_disponiveis
FROM animal a
JOIN instituicao i ON i.id_usuario = a.id_instituicao
WHERE a.status = 'Disponível'
GROUP BY i.razao_social
HAVING COUNT(*) >= 5
ORDER BY animais_disponiveis DESC, instituicao ASC;