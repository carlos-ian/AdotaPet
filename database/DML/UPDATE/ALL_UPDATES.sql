-- Atualização na Tabela usuario
UPDATE usuario SET senha = 'novaSenhaSegura123' WHERE email = 'joao.silva@email.com' AND senha = 'senhaAntiga123';
UPDATE usuario SET email = 'mariana.souza_novo@email.com' WHERE id_usuario = 2;
UPDATE usuario SET bairro = 'Jardim Amália', complemento = 'Apto 102' WHERE email = 'carlos.oliveira@email.com';
UPDATE usuario SET numero = '450' WHERE email = 'ana.santos@email.com';
UPDATE usuario SET cidade = 'Niterói', estado = 'RJ' WHERE id_usuario = 5;
UPDATE usuario SET cep = '24000-000' WHERE email = 'paula.lima@email.com' AND cidade = 'Niterói';
UPDATE usuario SET logradouro = 'Avenida Brasil' WHERE id_usuario = 7;

-- Atualização na Tabela usuario_telefone
UPDATE usuario_telefone SET telefone = '(11) 99999-0001' WHERE telefone = '(11) 98888-1111';
UPDATE usuario_telefone SET telefone = '(21) 99999-0002' WHERE telefone = '(21) 97777-2222';
UPDATE usuario_telefone SET telefone = '(31) 99999-0003' WHERE telefone = '(31) 96666-3333';
UPDATE usuario_telefone SET telefone = '(11) 99999-0004' WHERE telefone = '(11) 95555-4444';
UPDATE usuario_telefone SET telefone = '(11) 99999-0005' WHERE telefone = '(11) 95555-6666';

-- Atualização na Tabela instituicao
UPDATE instituicao SET razao_social = 'Associação de Proteção Animal Patas e Focinhos' WHERE cnpj = '12.345.678/0001-90';
UPDATE instituicao SET cnpj = '98.765.432/0001-10' WHERE id_usuario = 2;
UPDATE instituicao SET selo_verificacao = TRUE WHERE cnpj = '23.456.789/0001-01';
UPDATE instituicao SET razao_social = 'ONG Resgate Animal SP' WHERE id_usuario = 4;
UPDATE instituicao SET selo_verificacao = TRUE;

-- Atualização na Tabela adotante
UPDATE adotante SET nome = 'Mariana Souza Santos', tipo_residencia = 'Casa com Quintal' WHERE cpf = '222.333.444-55';
UPDATE adotante SET tipo_residencia = 'Apartamento' WHERE id_usuario = 1;
UPDATE adotante SET cpf = '111.222.333-99' WHERE id_usuario = 3;
UPDATE adotante SET tipo_residencia = 'Sítio' WHERE cpf = '333.444.555-66';
UPDATE adotante SET nome = 'Ana Paula Santos' WHERE id_usuario = 4;
UPDATE adotante SET tipo_residencia = 'Casa' WHERE cpf = '444.555.666-77';

-- Atualização na Tabela adotante_historico_pets
UPDATE adotante_historico_pets SET descricao = 'Possui experiência de 5 anos com cães de grande porte e adestramento básico.' WHERE id_historico = 1;
UPDATE adotante_historico_pets SET descricao = 'Teve dois gatos anteriormente, ambos com acompanhamento veterinário em dia.' WHERE id_historico = 2;
UPDATE adotante_historico_pets SET descricao = 'Cuida atualmente de um cão idoso resgatado das ruas.' WHERE id_historico = 3;
UPDATE adotante_historico_pets SET descricao = 'Já teve animais de pequeno porte em apartamento.' WHERE id_historico = 4;
UPDATE adotante_historico_pets SET descricao = 'Sem histórico prévio de pets, buscando o primeiro animal para adoção responsável.' WHERE id_historico = 5;

-- Atualização na Tabela animal
UPDATE animal SET status = 'Adotado', observacao = 'Adoção concluída com sucesso!' WHERE id_animal = 1;
UPDATE animal SET raca = 'Labrador Retriever', porte = 'Grande' WHERE nome = 'Rex' AND especie = 'Cão';
UPDATE animal SET idade = 3 WHERE id_animal = 3;
UPDATE animal SET porte = 'Médio', sexo = 'Macho' WHERE nome = 'Mingau' AND especie = 'Gato';
UPDATE animal SET observacao = 'Castrado, vacinado e vermifugado.' WHERE id_animal = 5;
UPDATE animal SET status = 'Em Tratamento' WHERE status = 'Pendente';
UPDATE animal SET raca = 'Vira-lata (SRD)' WHERE raca = 'SRD' OR raca IS NULL;
UPDATE animal SET idade = 5 WHERE nome = 'Thor' AND especie = 'Cão';
UPDATE animal SET porte = 'Pequeno' WHERE id_animal = 9;
UPDATE animal SET observacao = 'Muito dócil, se dá bem com outros animais e crianças.' WHERE id_animal = 10;
UPDATE animal SET status = 'Disponível' WHERE id_animal = 11;

-- Atualização na Tabela prontuario_veterinario
UPDATE prontuario_veterinario 
SET data_procedimento = '2025-01-15', descricao = 'Vacinação antirrábica e V10 aplicadas com sucesso.' 
WHERE id_animal = 1 AND tipo_procedimento = 'Vacinação';

UPDATE prontuario_veterinario 
SET descricao = 'Exame de sangue completo sem alterações clínicas significativas.' 
WHERE id_animal = 2 AND tipo_procedimento = 'Exame de Sangue';

UPDATE prontuario_veterinario 
SET data_procedimento = '2025-02-01', descricao = 'Castração realizada sem complicações pré ou pós-operatórias.' 
WHERE id_animal = 3 AND tipo_procedimento = 'Cirurgia de Castração';

UPDATE prontuario_veterinario 
SET descricao = 'Segunda dose de vermífugo administrada.' 
WHERE id_animal = 4 AND tipo_procedimento = 'Vermifugação';

UPDATE prontuario_veterinario 
SET descricao = 'Limpeza auricular e aplicação de medicação tópica.' 
WHERE id_animal = 5 AND tipo_procedimento = 'Consulta de Rotina';

UPDATE prontuario_veterinario 
SET data_procedimento = '2025-02-10' 
WHERE id_animal = 6 AND tipo_procedimento = 'Exame Parasitológico';

UPDATE prontuario_veterinario 
SET descricao = 'Procedimento cirúrgico de limpeza tártara concluído.' 
WHERE id_animal = 7 AND tipo_procedimento = 'Tratamento Odontológico';

-- Atualização na Tabela adota
UPDATE adota SET status = 'Aprovado', data_de_conclusao = '2025-02-15' WHERE id_adotante = 1 AND id_animal = 1;
UPDATE adota SET status = 'Em Análise' WHERE status = 'Reprovado';
UPDATE adota SET observacao_do_processo = 'Entrevista presencial realizada. Agendada visita domiciliar.' WHERE id_adotante = 2 AND id_animal = 3;
UPDATE adota SET status = 'Em Visita Domiciliar' WHERE status = 'Solicitado';
UPDATE adota SET data_solicitacao = '2025-01-20', observacao_do_processo = 'Documentação validada com sucesso.' WHERE id_adotante = 3 AND id_animal = 4;
UPDATE adota SET status = 'Cancelado', observacao_do_processo = 'Desistência por parte do adotante.' WHERE id_adotante = 4 AND id_animal = 5;
UPDATE adota SET status = 'Concluído', data_de_conclusao = '2025-02-20' WHERE id_adotante = 5 AND id_animal = 6;
UPDATE adota SET observacao_do_processo = 'Aguardando envio do comprovante de residência.' WHERE status = 'Pendente';
UPDATE adota SET data_solicitacao = '2025-02-01' WHERE id_adotante = 6 AND id_animal = 7;
UPDATE adota SET status = 'Aprovado' WHERE id_animal = 8 AND status = 'Em Análise';

-- Atualização na Tabela apadrinha
UPDATE apadrinha SET tipo_de_contribuicao = 'Financeira', valor_recorrente = 150.00 WHERE id_adotante = 1 AND id_animal = 2;
UPDATE apadrinha SET frequencia = 'Mensal' WHERE frequencia = 'Bimestral';
UPDATE apadrinha SET valor_recorrente = 200.00 WHERE id_adotante = 3 AND id_animal = 4;
UPDATE apadrinha SET tipo_de_contribuicao = 'Ração e Medicamentos', valor_recorrente = NULL WHERE id_adotante = 4 AND id_animal = 5;
UPDATE apadrinha SET data_inicio = '2025-01-01' WHERE id_adotante = 2 AND id_animal = 3;
UPDATE apadrinha SET valor_recorrente = 100.00 WHERE id_adotante = 5 AND id_animal = 6;
UPDATE apadrinha SET frequencia = 'Semestral' WHERE id_adotante = 6 AND id_animal = 7;
UPDATE apadrinha SET tipo_de_contribuicao = 'Financeira' WHERE id_animal = 8;
UPDATE apadrinha SET valor_recorrente = 75.00 WHERE id_adotante = 7 AND id_animal = 9;
UPDATE apadrinha SET frequencia = 'Mensal' WHERE id_adotante = 8 AND id_animal = 10;
