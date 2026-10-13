-- Relatório geral relacionando Pet, Instituição responsável, Processo de Adoção e Adotante
SELECT 
    an.nome AS nome_pet,
    an.especie,
    i.razao_social AS ong_responsavel,
    a.nome AS nome_adotante,
    ad.status AS status_adocao,
    ad.data_de_solicitacao
FROM Animal an
INNER JOIN Instituicao i ON an.id_instituicao = i.id_usuario
INNER JOIN Adota ad ON an.id_animal = ad.id_animal
INNER JOIN Adotante a ON ad.id_adotante = a.id_usuario;