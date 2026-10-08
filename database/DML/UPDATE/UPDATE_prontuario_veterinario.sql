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