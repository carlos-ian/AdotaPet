-- Remoção na Tabela usuario
DELETE FROM usuario WHERE email = 'usuario.inativo1@email.com';
DELETE FROM usuario WHERE email = 'teste.cancelado@email.com';
DELETE FROM usuario WHERE id_usuario = 13;
DELETE FROM usuario WHERE id_usuario = 14;
DELETE FROM usuario WHERE id_usuario = 15;

-- Remoção na Tabela usuario_telefone
DELETE FROM usuario_telefone WHERE telefone = '(11) 98888-1111';
DELETE FROM usuario_telefone WHERE telefone = '(21) 97777-2222';
DELETE FROM usuario_telefone WHERE telefone = '(31) 96666-3333';
DELETE FROM usuario_telefone WHERE telefone = '(11) 95555-4444';
DELETE FROM usuario_telefone WHERE telefone = '(11) 95555-6666';

-- Remoção na Tabela instituicao
DELETE FROM instituicao WHERE cnpj = '99.888.777/0001-66';
DELETE FROM instituicao WHERE id_usuario = 5;

-- Remoção na Tabela adotante
DELETE FROM adotante WHERE cpf = '999.888.777-66';
DELETE FROM adotante WHERE cpf = '888.777.666-55';
DELETE FROM adotante WHERE cpf = '777.666.555-44';
DELETE FROM adotante WHERE id_usuario = 9;
DELETE FROM adotante WHERE id_usuario = 10;

-- Remoção na Tabela adotante_historico_pets
DELETE FROM adotante_historico_pets WHERE id_historico = 1;
DELETE FROM adotante_historico_pets WHERE id_historico = 2;
DELETE FROM adotante_historico_pets WHERE id_historico = 3;
DELETE FROM adotante_historico_pets WHERE id_historico = 4;
DELETE FROM adotante_historico_pets WHERE id_historico = 5;

-- Remoção na Tabela animal
DELETE FROM animal WHERE nome = 'PetTeste' AND especie = 'Cão';
DELETE FROM animal WHERE status = 'Obito';
DELETE FROM animal WHERE id_animal = 23;
DELETE FROM animal WHERE id_animal = 24;
DELETE FROM animal WHERE id_animal = 25;

-- Remoção na Tabela prontuario_veterinario
DELETE FROM prontuario_veterinario 
WHERE id_animal = 1 AND data_procedimento = '2025-01-10' AND tipo_procedimento = 'Triagem e Exame Físico';

DELETE FROM prontuario_veterinario 
WHERE id_animal = 6 AND data_procedimento = '2025-01-05' AND tipo_procedimento = 'Exame de Sangue';

DELETE FROM prontuario_veterinario 
WHERE id_animal = 2 AND data_procedimento = '2025-01-18' AND tipo_procedimento = 'Vermifugação';

DELETE FROM prontuario_veterinario 
WHERE id_animal = 7 AND data_procedimento = '2025-02-05' AND tipo_procedimento = 'Vacinação';

DELETE FROM prontuario_veterinario 
WHERE id_animal = 14 AND data_procedimento = '2025-01-28' AND tipo_procedimento = 'Exame Parasitológico';

-- Remoção na Tabela adota
DELETE FROM adota WHERE status = 'Cancelado';
DELETE FROM adota WHERE id_adotante = 6 AND id_animal = 11;
DELETE FROM adota WHERE id_adotante = 8 AND id_animal = 20;
DELETE FROM adota WHERE id_adotante = 6 AND id_animal = 13;
DELETE FROM adota WHERE id_adotante = 10 AND id_animal = 2;

-- Remoção na Tabela apadrinha
DELETE FROM apadrinha WHERE valor_recorrente = 0.00;
DELETE FROM apadrinha WHERE id_adotante = 6 AND id_animal = 1;
DELETE FROM apadrinha WHERE id_adotante = 7 AND id_animal = 2;
DELETE FROM apadrinha WHERE id_adotante = 8 AND id_animal = 4;
DELETE FROM apadrinha WHERE id_adotante = 10 AND id_animal = 5;
