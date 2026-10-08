UPDATE instituicao 
SET razao_social = 'Associação de Proteção Animal Patas e Focinhos' 
WHERE cnpj = '12.345.678/0001-90';

UPDATE instituicao 
SET cnpj = '98.765.432/0001-10' 
WHERE id_usuario = 2;

UPDATE instituicao 
SET selo_verificacao = TRUE 
WHERE cnpj = '23.456.789/0001-01';

UPDATE instituicao 
SET razao_social = 'ONG Resgate Animal SP' 
WHERE id_usuario = 4;

UPDATE instituicao 
SET selo_verificacao = TRUE;