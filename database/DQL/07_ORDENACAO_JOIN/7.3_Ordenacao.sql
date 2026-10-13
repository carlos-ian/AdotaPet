-- 7.3 Processos de adoção por status e data de solicitação mais recente
SELECT ad.status, ado.nome AS adotante, u.cidade AS cidade_adotante,
       a.nome AS animal, a.especie, ad.data_de_solicitacao, ad.data_de_conclusao
FROM adota ad
JOIN adotante ado ON ado.id_usuario = ad.id_adotante
JOIN usuario u    ON u.id_usuario  = ado.id_usuario
JOIN animal a     ON a.id_animal   = ad.id_animal
ORDER BY ad.status ASC, ad.data_de_solicitacao DESC;
