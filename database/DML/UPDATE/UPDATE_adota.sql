UPDATE adota 
SET status = 'Aprovado', data_de_conclusao = '2025-02-15' 
WHERE id_adotante = 1 AND id_animal = 1;

UPDATE adota 
SET status = 'Em Análise' 
WHERE status = 'Reprovado';

UPDATE adota 
SET observacao_do_processo = 'Entrevista presencial realizada. Agendada visita domiciliar.' 
WHERE id_adotante = 2 AND id_animal = 3;

UPDATE adota 
SET status = 'Em Visita Domiciliar' 
WHERE status = 'Solicitado';

UPDATE adota 
SET data_solicitacao = '2025-01-20', observacao_do_processo = 'Documentação validada com sucesso.' 
WHERE id_adotante = 3 AND id_animal = 4;

UPDATE adota 
SET status = 'Cancelado', observacao_do_processo = 'Desistência por parte do adotante.' 
WHERE id_adotante = 4 AND id_animal = 5;

UPDATE adota 
SET status = 'Concluído', data_de_conclusao = '2025-02-20' 
WHERE id_adotante = 5 AND id_animal = 6;

UPDATE adota 
SET observacao_do_processo = 'Aguardando envio do comprovante de residência.' 
WHERE status = 'Pendente';

UPDATE adota 
SET data_solicitacao = '2025-02-01' 
WHERE id_adotante = 6 AND id_animal = 7;

UPDATE adota 
SET status = 'Aprovado' 
WHERE id_animal = 8 AND status = 'Em Análise';