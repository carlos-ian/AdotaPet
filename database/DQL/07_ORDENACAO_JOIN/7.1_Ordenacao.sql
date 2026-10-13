-- 7.1 Animais com instituição e cidade, por instituição, espécie e idade (mais velho primeiro)
SELECT i.razao_social AS instituicao, u.cidade, a.nome AS animal, a.especie, a.idade, a.status
FROM animal a
JOIN instituicao i ON i.id_usuario = a.id_instituicao
JOIN usuario u     ON u.id_usuario = i.id_usuario
ORDER BY i.razao_social ASC, a.especie ASC, a.idade DESC;
