-- Lista apadrinhamentos vinculandos a Padrinhos, Contribuições e Pets
SELECT 
    a.nome AS nome_padrinho,
	a.cpf AS cpf_padrinho,
    an.nome AS nome_pet,
    an.especie,
    ap.tipo_de_contribuicao,
    ap.valor_recorrente,
    ap.frequencia,
    ap.status AS status_apadrinhamento,
    ap.data_de_inicio
FROM Adotante a
INNER JOIN Apadrinha ap ON a.id_usuario = ap.id_adotante
INNER JOIN Animal an ON ap.id_animal = an.id_animal;