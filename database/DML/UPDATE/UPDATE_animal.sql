UPDATE animal 
SET status = 'Adotado', observacao = 'Adoção concluída com sucesso!' 
WHERE id_animal = 1;

UPDATE animal 
SET raca = 'Labrador Retriever', porte = 'Grande' 
WHERE nome = 'Rex' AND especie = 'Cão';

UPDATE animal 
SET idade = 3 
WHERE id_animal = 3;

UPDATE animal 
SET porte = 'Médio', sexo = 'Macho' 
WHERE nome = 'Mingau' AND especie = 'Gato';

UPDATE animal 
SET observacao = 'Castrado, vacinado e vermifugado.' 
WHERE id_animal = 5;

UPDATE animal 
SET status = 'Em Tratamento' 
WHERE status = 'Pendente';

UPDATE animal 
SET raca = 'Vira-lata (SRD)' 
WHERE raca = 'SRD' OR raca IS NULL;

UPDATE animal 
SET idade = 5 
WHERE nome = 'Thor' AND especie = 'Cão';

UPDATE animal 
SET porte = 'Pequeno' 
WHERE id_animal = 9;

UPDATE animal 
SET observacao = 'Muito dócil, se dá bem com outros animais e crianças.' 
WHERE id_animal = 10;

UPDATE animal 
SET status = 'Disponível' 
WHERE id_animal = 11;