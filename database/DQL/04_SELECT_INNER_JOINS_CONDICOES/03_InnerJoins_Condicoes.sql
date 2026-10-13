-- Inner Joins com Usuario + Usuario_Telefone + Adotante + Apadrinha + Animal (5 Tabelas)
SELECT 
    u.email,
    ut.telefone,
    a.nome AS nome_padrinho,
    an.nome AS nome_pet,
    ap.valor_recorrente
FROM Usuario u
INNER JOIN Usuario_Telefone ut ON u.id_usuario = ut.id_usuario
INNER JOIN Adotante a ON u.id_usuario = a.id_usuario
INNER JOIN Apadrinha ap ON a.id_usuario = ap.id_adotante
INNER JOIN Animal an ON ap.id_animal = an.id_animal
WHERE ap.status = 'Ativo' 
  AND ap.frequencia = 'Mensal';

-- Mostra apenas os apadrinhamentos ativos com frequência mensal (condição)
-- trazendo informações do usuário, telefone, padrinho, animal apadrinhado e valor recorrente 
-- do apadrinhamento