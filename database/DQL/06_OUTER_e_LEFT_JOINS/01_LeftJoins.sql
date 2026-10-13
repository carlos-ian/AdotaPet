-- 6.1 LEFT JOIN: todos os animais e, se houver, o processo de adoção e o adotante
SELECT a.id_animal, a.nome AS animal, a.especie, a.status AS status_animal,
       ad.status AS status_adocao, ado.nome AS adotante, ad.data_de_solicitacao
FROM animal a
LEFT JOIN adota ad     ON ad.id_animal = a.id_animal
LEFT JOIN adotante ado ON ado.id_usuario = ad.id_adotante;
