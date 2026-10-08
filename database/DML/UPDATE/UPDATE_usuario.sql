UPDATE usuario 
SET senha = 'novaSenhaSegura123' 
WHERE email = 'joao.silva@email.com' AND senha = 'senhaAntiga123';

UPDATE usuario 
SET email = 'mariana.souza_novo@email.com' 
WHERE id_usuario = 2;

UPDATE usuario 
SET bairro = 'Jardim Amália', complemento = 'Apto 102' 
WHERE email = 'carlos.oliveira@email.com';

UPDATE usuario 
SET numero = '450' 
WHERE email = 'ana.santos@email.com';

UPDATE usuario 
SET cidade = 'Niterói', estado = 'RJ' 
WHERE id_usuario = 5;

UPDATE usuario 
SET cep = '24000-000' 
WHERE email = 'paula.lima@email.com' AND cidade = 'Niterói';

UPDATE usuario 
SET logradouro = 'Avenida Brasil' 
WHERE id_usuario = 7;