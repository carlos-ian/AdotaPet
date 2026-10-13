-- 2.0 LEFT JOIN + IS NULL: animais que não têm padrinho
SELECT a.id_animal, a.nome AS animal, a.especie, i.razao_social AS instituicao
FROM animal a
JOIN instituicao i     ON i.id_usuario = a.id_instituicao
LEFT JOIN apadrinha ap ON ap.id_animal = a.id_animal
WHERE ap.id_animal IS NULL;
