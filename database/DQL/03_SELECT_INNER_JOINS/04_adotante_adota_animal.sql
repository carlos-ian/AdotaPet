-- Lista processos de adoção vinculando Adotante, Processo e Pet
SELECT 
    a.nome AS nome_adotante,
    a.cpf,
    an.nome AS nome_pet,
    an.especie,
    ad.status AS status_adocao,
    ad.data_de_solicitacao,
    ad.observacao_do_processo
FROM Adotante a
INNER JOIN Adota ad ON a.id_usuario = ad.id_adotante
INNER JOIN Animal an ON ad.id_animal = an.id_animal;