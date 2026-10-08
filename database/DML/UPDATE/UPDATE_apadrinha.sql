UPDATE apadrinha 
SET tipo_de_contribuicao = 'Financeira', valor_recorrente = 150.00 
WHERE id_adotante = 1 AND id_animal = 2;

UPDATE apadrinha 
SET frequencia = 'Mensal' 
WHERE frequencia = 'Bimestral';

UPDATE apadrinha 
SET valor_recorrente = 200.00 
WHERE id_adotante = 3 AND id_animal = 4;

UPDATE apadrinha 
SET tipo_de_contribuicao = 'Ração e Medicamentos', valor_recorrente = NULL 
WHERE id_adotante = 4 AND id_animal = 5;

UPDATE apadrinha 
SET data_inicio = '2025-01-01' 
WHERE id_adotante = 2 AND id_animal = 3;

UPDATE apadrinha 
SET valor_recorrente = 100.00 
WHERE id_adotante = 5 AND id_animal = 6;

UPDATE apadrinha 
SET frequencia = 'Semestral' 
WHERE id_adotante = 6 AND id_animal = 7;

UPDATE apadrinha 
SET tipo_de_contribuicao = 'Financeira' 
WHERE id_animal = 8;

UPDATE apadrinha 
SET valor_recorrente = 75.00 
WHERE id_adotante = 7 AND id_animal = 9;

UPDATE apadrinha 
SET frequencia = 'Mensal' 
WHERE id_adotante = 8 AND id_animal = 10;