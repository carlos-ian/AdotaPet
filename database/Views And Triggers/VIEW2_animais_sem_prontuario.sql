CREATE OR REPLACE VIEW vw_animais_sem_prontuario AS
SELECT 
    a.id_animal,
    a.nome AS nome_animal,
    a.especie,
    a.status AS status_animal,
    i.razao_social AS nome_instituicao
FROM animal a
INNER JOIN instituicao i ON a.id_instituicao = i.id_usuario
WHERE NOT EXISTS (
    SELECT 1 
    FROM prontuario_veterinario pv 
    WHERE pv.id_animal = a.id_animal
);