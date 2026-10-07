INSERT INTO adota (id_adotante, id_animal, status, data_de_solicitacao, data_de_conclusao, observacao_do_processo) VALUES
-- ==========================================
-- PROCESSOS CONCLUÍDOS (Aprovação e Adoção Finalizada)
-- ==========================================
(6, 13, 'Aprovado', '2025-01-05', '2025-01-15', 'Entrevista realizada, vistoria residencial ok. Animal entregue com sucesso.'),
(8, 6, 'Aprovado', '2025-01-10', '2025-01-20', 'Adotante possui quintal grande e experiência com cães de grande porte. Adoção concluída.'),
(10, 2, 'Aprovado', '2025-01-12', '2025-01-22', 'Telas de proteção confirmadas no apartamento. Gatinha adaptada.'),
(12, 19, 'Aprovado', '2025-02-01', '2025-02-10', 'Família com espaço adequado para Golden Retriever. Termo de adoção assinado.'),
(7, 5, 'Aprovado', '2025-01-25', '2025-02-02', 'Termo assinado e orientações de cuidados com coelhos repassadas.'),
(10, 10, 'Aprovado', '2025-01-18', '2025-01-28', 'Verificado viveiro seguro para calopsita. Processo finalizado.'),
(15, 22, 'Aprovado', '2025-01-30', '2025-02-08', 'Cão idoso adotado por família experiente. Termo assinado.'),

-- ==========================================
-- PROCESSOS EM ANÁLISE / EM ANDAMENTO
-- ==========================================
(7, 1, 'Em Análise', '2025-02-10', NULL, 'Aguardando agendamento da entrevista virtual com a ONG.'),
(9, 7, 'Em Análise', '2025-02-12', NULL, 'Formulário inicial recebido. Em fase de verificação de documentos.'),
(11, 3, 'Em Análise', '2025-02-14', NULL, 'Avaliando se o adotante possui ambiente adequado para aves.'),
(13, 21, 'Em Análise', '2025-02-15', NULL, 'Visita domiciliar agendada para a próxima semana.'),
(9, 9, 'Em Análise', '2025-02-16', NULL, 'Formulário recebido para adoção de hamster, aguardando fotos do alojamento.'),
(11, 14, 'Em Análise', '2025-02-18', NULL, 'Análise de autorização de órgãos ambientais para posse responsável de papagaio.'),

-- ==========================================
-- PROCESSOS RECUSADOS / NÃO APROVADOS
-- ==========================================
(14, 4, 'Recusado', '2025-01-15', '2025-01-18', 'Perfil incompatível: presença de animais territoriais no imóvel.'),
(15, 8, 'Recusado', '2025-01-20', '2025-01-23', 'Incompatibilidade com o tipo de residência informado no cadastro.'),
(14, 18, 'Recusado', '2025-02-01', '2025-02-04', 'Falta de tela de proteção adequada em recinto externo.'),

-- ==========================================
-- PROCESSOS CANCELADOS PELO ADOTANTE
-- ==========================================
(6, 11, 'Cancelado', '2025-01-08', '2025-01-12', 'Adotante desistiu do processo por motivos de mudança residencial.'),
(8, 20, 'Cancelado', '2025-02-05', '2025-02-09', 'Adotante optou por adiar adoção devido a viagens de trabalho.');