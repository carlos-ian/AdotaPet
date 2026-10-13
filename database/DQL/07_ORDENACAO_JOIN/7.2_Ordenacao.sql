-- 7.2 Prontuário veterinário do mais recente ao mais antigo
SELECT pv.data_procedimento, pv.tipo_procedimento, a.nome AS animal, a.especie,
       i.razao_social AS instituicao
FROM prontuario_veterinario pv
JOIN animal a      ON a.id_animal = pv.id_animal
JOIN instituicao i ON i.id_usuario = a.id_instituicao
ORDER BY pv.data_procedimento DESC, a.nome ASC;
