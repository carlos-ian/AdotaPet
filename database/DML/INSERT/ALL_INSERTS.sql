-- Inserção na Tabela usuario
INSERT INTO usuario (email, senha, rua, numero, bairro, cep, cidade, estado, complemento, tipo_usuario)  VALUES
('contato@patasdaamazonia.org', 'Inst#123', 'Avenida Efigênio Salles', '1200', 'Aleixo', '69057-050', 'Manaus', 'AM', 'Galpão A', 'Instituição'),
('atendimento@patinhassp.org', 'Inst#456', 'Avenida Paulista', '1000', 'Bela Vista', '01310-100', 'São Paulo', 'SP', 'Conjunto 42', 'Instituição'),
('adm@caesegatosrio.org', 'Inst#789', 'Rua Visconde de Pirajá', '405', 'Ipanema', '22410-003', 'Rio de Janeiro', 'RJ', 'Loja 02', 'Instituição'),
('contato@resgatebh.org', 'Inst#101', 'Avenida Afonso Pena', '1500', 'Centro', '30130-005', 'Belo Horizonte', 'MG', 'Sala 302', 'Instituição'),
('adocaocapitais@ongsul.org', 'Inst#202', 'Rua XV de Novembro', '88', 'Centro', '80020-310', 'Curitiba', 'PR', NULL, 'Instituição'),

('lucas.silva@email.com', 'K9#mP2x!', 'Avenida Beira Mar', '2100', 'Meireles', '60165-121', 'Fortaleza', 'CE', 'Apto 802', 'Adotante'),
('mariana.santos@email.com', 'vR8$qL1w', 'Rua das Flores', '250', 'Jardim Primavera', '13080-000', 'Campinas', 'SP', 'Bloco B, Apto 12', 'Adotante'),
('carlos.oliveira@email.com', 'T7@aZ9uQ', 'Avenida Boa Viagem', '3500', 'Boa Viagem', '51020-001', 'Recife', 'PE', 'Apto 1501', 'Adotante'),
('ana.pereira@email.com', 'mX3!nK5p', 'Rua dos Andradas', '600', 'Centro Histórico', '90020-002', 'Porto Alegre', 'RS', 'Apto 33', 'Adotante'),
('beatriz.lima@email.com', 'B2#vJ9tL', 'Avenida Epitácio Pessoa', '850', 'Bairro dos Estados', '58030-000', 'João Pessoa', 'PB', NULL, 'Adotante'),
('rodrigo.almeida@email.com', 'gW6&rD4x', 'Rua das Laranjeiras', '12', 'Laranjeiras', '22240-000', 'Rio de Janeiro', 'RJ', 'Fundos', 'Adotante'),
('fernanda.costa@email.com', 'zP1*cM8y', 'Avenida do Cordeiro', '45', 'Cordeiro', '50721-000', 'Recife', 'PE', NULL, 'Adotante'),
('rafael.gomes@email.com', 'H5$kS3vN', 'Rua Bahia', '780', 'Savassi', '30160-011', 'Belo Horizonte', 'MG', 'Apto 201', 'Adotante'),
('juliana.martins@email.com', 'qL9#fT2w', 'Avenida Getúlio Vargas', '900', 'Menino Deus', '90150-002', 'Porto Alegre', 'RS', 'Apto 504', 'Adotante'),
('diego.rocha@email.com', 'X4!bR7mZ', 'Rua Mato Grosso', '140', 'Siqueira Campos', '49075-100', 'Aracaju', 'SE', NULL, 'Adotante');

-- Inserção na Tabela usuario_telefone
INSERT INTO usuario_telefone (id_usuario, telefone) VALUES
(1, '(92) 98111-2020'),
(1, '(92) 3234-5678'),
(2, '(11) 97222-3030'),
(2, '(11) 3010-4040'),
(3, '(21) 96333-4040'),
(4, '(31) 95444-5050'),
(5, '(41) 94555-6060'),
(6, '(85) 99123-4567'),
(7, '(19) 98234-5678'),
(8, '(81) 97345-6789'),
(8, '(81) 98877-6655'),
(9, '(51) 96456-7890'),
(10, '(83) 95567-8901'),
(11, '(21) 94678-9012'),
(12, '(81) 93789-0123'),
(13, '(31) 92890-1234'),
(14, '(51) 91901-2345'),
(15, '(79) 99012-3456');

-- Inserção na Tabela instituicao
INSERT INTO instituicao (id_usuario, cnpj, razao_social, selo_verificacao) VALUES
(1, '12.345.678/0001-90', 'Associação Patas da Amazônia', TRUE),
(2, '23.456.789/0001-01', 'ONG Patinhas São Paulo', TRUE),
(3, '34.567.890/0001-12', 'Instituto Cães e Gatos Rio', FALSE),
(4, '45.678.901/0001-23', 'Projeto Resgate Animal BH', TRUE),
(5, '56.789.012/0001-34', 'Associação Adoção Sul', FALSE);

-- Inserção na Tabela adotante
INSERT INTO adotante (id_usuario, nome, cpf, tipo_residencia) VALUES
(6, 'Lucas Silva', '111.222.333-01', 'Apartamento'),
(7, 'Mariana Santos', '222.333.444-02', 'Casa Térrea'),
(8, 'Carlos Oliveira', '333.444.555-03', 'Casa com quintal'),
(9, 'Ana Pereira', '444.555.666-04', 'Apartamento'),
(10, 'Beatriz Lima', '555.666.777-05', 'Casa com quintal'),
(11, 'Rodrigo Almeida', '666.777.888-06', 'Chácara'),
(12, 'Fernanda Costa', '777.888.999-07', 'Duplex'),
(13, 'Rafael Gomes', '888.999.000-08', 'Condomínio'),
(14, 'Juliana Martins', '999.000.111-09', 'Apartamento'),
(15, 'Diego Rocha', '000.111.222-10', 'Sobrado');

-- Inserção na Tabela adotante_historico_pets
INSERT INTO adotante_historico_pets (id_usuario, descricao) VALUES
(6, 'Já teve um cachorro da raça Poodle por 12 anos. Experiência com cuidados básicos e vacinação em dia.'),
(7, 'Teve dois gatos resgatados da rua que viveram até a velhice. Conhecimento em tela de proteção para apartamento.'),
(8, 'Possui histórico de adoção de cães de grande porte. Casa ampla com quintal todo cercado.'),
(9, 'Cuidou de um gato Siamês durante 10 anos. Experiência com ração especial e acompanhamento veterinário.'),
(10, 'Sempre teve cães em casa familiar. Experiência com adestramento básico e passeios diários.'),
(11, 'Cuidou de animais em sítio/chácara. Experiência no manejo de cães de médio e grande porte.'),
(12, 'Primeira experiência como tutora principal, mas ajudava nos cuidados do cachorro dos pais.'),
(13, 'Teve um cachorro vira-lata por 15 anos. Experiência completa com rotina médica e alimentação.'),
(14, 'Já teve gatos em apartamento. Experiência com enriquecimento ambiental e veterinário frequente.'),
(15, 'Teve cães de porte médio na infância e juventude. Espaço amplo disponível para novo pet.');

-- Inserção na Tabela animal
INSERT INTO animal (id_instituicao, nome, especie, raca, idade, porte, sexo, status, observacao) VALUES
(1, 'Thor', 'Cão', 'Vira-lata (SRD)', 3, 'Médio', 'M', 'Disponível', 'Muito carinhoso e dócil com crianças.'),
(1, 'Mimi', 'Gato', 'Siamês', 2, 'Pequeno', 'F', 'Disponível', 'Gosta de ambientes tranquilos.'),
(1, 'Louro', 'Papagaio', 'Papagaio-verdadeiro', 5, 'Pequeno', 'M', 'Disponível', 'Muito tagarela, possui documentação de manejo/resgate.'),
(1, 'Bochecha', 'Hamster', 'Sirio', 1, 'Pequeno', 'M', 'Disponível', 'Muito ativo, gosta de rodinha de exercício.'),
(1, 'Pipoca', 'Coelho', 'Mini Lion Head', 1, 'Pequeno', 'F', 'Disponível', 'Muito dócil e acostumada com manuseio.'),
(1, 'Apolo', 'Cão', 'Golden Retriever', 4, 'Grande', 'M', 'Em processo de adoção', 'Extremamente dócil e brincalhão.'),
(1, 'Jade', 'Gato', 'Persa', 3, 'Pequeno', 'F', 'Disponível', 'Nível de energia baixo, ideal para apartamento.'),

(2, 'Rex', 'Cão', 'Pastor Alemão', 5, 'Grande', 'M', 'Em processo de adoção', 'Excelente cão de guarda e companheiro.'),
(2, 'Luna', 'Gato', 'Persa', 1, 'Pequeno', 'F', 'Disponível', 'Gatinha muito brincalhona e castrada.'),
(2, 'Kiko', 'Papagaio', 'Papagaio-da-várzea', 8, 'Pequeno', 'M', 'Disponível', 'Resgatado de apreensão, sociável e saudável.'),
(2, 'Amendoim', 'Hamster', 'Anão Russo', 1, 'Pequeno', 'M', 'Disponível', 'Pequeno e muito ágil.'),
(2, 'Pingo', 'Calopsita', 'Silvestre', 2, 'Pequeno', 'M', 'Disponível', 'Asas aparadas e habituado a ficar no ombro.'),
(2, 'Belinha', 'Cão', 'Poodle', 6, 'Pequeno', 'F', 'Disponível', 'Calma, ótima para idosos.'),

(3, 'Bob', 'Cão', 'Poodle', 4, 'Pequeno', 'M', 'Disponível', 'Gosta de passear e se dá bem com outros cães.'),
(3, 'Nina', 'Gato', 'Vira-lata (SRD)', 2, 'Pequeno', 'F', 'Adotado', 'Adotada recentemente, dócil e carinhosa.'),
(3, 'Zezé', 'Papagaio', 'Papagaio-chauá', 4, 'Pequeno', 'M', 'Disponível', 'Muito curioso e imita sons de campainha.'),
(3, 'Peluche', 'Coelho', 'Holandês', 2, 'Pequeno', 'M', 'Disponível', 'Castrado e acostumado a usar caixinha de horta.'),
(3, 'Tom', 'Gato', 'Angorá', 3, 'Pequeno', 'M', 'Disponível', 'Pelagem longa, precisa de escovação frequente.'),

(4, 'Mel', 'Cão', 'Golden Retriever', 2, 'Grande', 'F', 'Disponível', 'Muito enérgica, precisa de espaço para correr.'),
(4, 'Simba', 'Gato', 'Vira-lata (SRD)', 1, 'Pequeno', 'M', 'Disponível', 'Filhote resgatado, vacinado e vermifugado.'),
(4, 'Fofinho', 'Hamster', 'SÍrio', 1, 'Pequeno', 'M', 'Disponível', 'Sociável e acostumado com crianças.'),
(4, 'Cacau', 'Calopsita', 'Lutino', 2, 'Pequeno', 'F', 'Disponível', 'Assobia trechos de músicas.'),

(5, 'Pipoca', 'Cão', 'Beagle', 3, 'Médio', 'F', 'Disponível', 'Muito curiosa e sociável com outros pets.'),
(5, 'Fred', 'Cão', 'Vira-lata (SRD)', 6, 'Médio', 'M', 'Disponível', 'Cão adulto muito calmo e companheiro.'),
(5, 'Pita', 'Porquinho-da-Índia', 'Inglês', 1, 'Pequeno', 'F', 'Disponível', 'Muito tranquila e acostumada a comer verduras.');

-- Inserção na Tabela prontuario_veterinario
INSERT INTO prontuario_veterinario (id_animal, data_procedimento, tipo_procedimento, descricao) VALUES
(1, '2025-01-10', 'Triagem e Exame Físico', 'Avaliação inicial pós-resgate. Animal sem lesões graves.'),
(1, '2025-01-20', 'Vacinação', 'Aplicação da vacina V10 (1ª dose) e Antirrábica.'),
(1, '2025-02-15', 'Consulta de Acompanhamento', 'Exame físico completo. Animal dócil e apto para adoção.'),
(6, '2025-01-05', 'Exame de Sangue', 'Hemograma completo de rotina. Taxas dentro da normalidade.'),
(6, '2025-01-15', 'Vacinação', 'Aplicação da vacina Antirrábica e V10.'),
(6, '2025-02-01', 'Consulta Geral', 'Check-up de rotina para liberação de adoção.'),
(2, '2025-01-18', 'Vermifugação', 'Administração de vermífugo de amplo espectro em dose única.'),
(2, '2025-01-25', 'Castração', 'Procedimento cirúrgico de ovariossalpingectomia realizado sem intercorrências.'),
(7, '2025-01-22', 'Castração', 'Castração preventiva realizada com sucesso. Boa recuperação pós-anestésica.'),
(7, '2025-02-05', 'Vacinação', 'Aplicação de vacina Quintupla Felina (V5).'),
(14, '2025-01-28', 'Exame Parasitológico', 'Análise de fezes para verificação de parasitas aviários. Resultado negativo.'),
(14, '2025-02-10', 'Consulta Veterinária Especializada', 'Check-up de rotina para aves, avaliação de bico e penas.'),
(19, '2025-01-12', 'Vacinação', 'Aplicação da vacina V10 (1ª dose).'),
(19, '2025-02-02', 'Vacinação', 'Reforço da vacina V10 e aplicação de Antirrábica.'),
(20, '2025-01-15', 'Vermifugação', 'Primeira dose de vermífugo infantil administrada.'),
(20, '2025-02-01', 'Consulta Geral', 'Avaliação de ganho de peso e saúde geral do filhote.'),
(3, '2025-02-01', 'Consulta Veterinária Especializada', 'Avaliação de penas, bico e estado nutricional de ave resgatada.'),
(4, '2025-02-05', 'Exame Físico', 'Avaliação de dentes incisivos e pesagem (45g). Excelente estado de saúde.'),
(5, '2025-01-18', 'Vacinação', 'Aplicação de vacina preventiva contra Mixomatose.'),
(8, '2025-01-30', 'Exame Físico', 'Acompanhamento clínico geral de ave de apreensão.'),
(9, '2025-02-08', 'Exame Físico', 'Check-up básico, pesagem e inspeção da pelagem.'),
(10, '2025-02-03', 'Aparagem de Penas', 'Aparagem de penas de voo realizada para segurança no manejo doméstico.'),
(11, '2025-01-14', 'Vacinação', 'Reforço da vacina Antirrábica para cães sênior.'),
(12, '2025-01-26', 'Limpeza TÁrtaro', 'Procedimento de profilaxia periodontal sem complicações.'),
(13, '2025-01-08', 'Vacinação', 'Aplicação de vacina Tríplice Felina (V3).'),
(15, '2025-01-21', 'Castração', 'Procedimento de orquiectomia realizado em coelho jovem.'),
(16, '2025-02-04', 'Consulta Dermatológica', 'Inspeção de pelagem e dermatite de pulga leve tratada com medicação tópica.'),
(17, '2025-02-11', 'Exame Físico', 'Exame físico de rotina. Sem alterações detectadas.'),
(18, '2025-02-09', 'Consulta Veterinária Especializada', 'Avaliação comportamental e nutricional.'),
(21, '2025-01-19', 'Vacinação', 'Aplicação da vacina V10 e vermifugação.'),
(22, '2025-01-11', 'Consulta Geral', 'Check-up geriátrico. Animal saudável para a idade.');

-- Inserção na Tabela adota
INSERT INTO adota (id_adotante, id_animal, status, data_de_solicitacao, data_de_conclusao, observacao_do_processo) VALUES
(6, 13, 'Aprovado', '2025-01-05', '2025-01-15', 'Entrevista realizada, vistoria residencial ok. Animal entregue com sucesso.'),
(8, 6, 'Aprovado', '2025-01-10', '2025-01-20', 'Adotante possui quintal grande e experiência com cães de grande porte. Adoção concluída.'),
(10, 2, 'Aprovado', '2025-01-12', '2025-01-22', 'Telas de proteção confirmadas no apartamento. Gatinha adaptada.'),
(12, 19, 'Aprovado', '2025-02-01', '2025-02-10', 'Família com espaço adequado para Golden Retriever. Termo de adoção assinado.'),
(7, 5, 'Aprovado', '2025-01-25', '2025-02-02', 'Termo assinado e orientações de cuidados com coelhos repassadas.'),
(10, 10, 'Aprovado', '2025-01-18', '2025-01-28', 'Verificado viveiro seguro para calopsita. Processo finalizado.'),
(15, 22, 'Aprovado', '2025-01-30', '2025-02-08', 'Cão idoso adotado por família experiente. Termo assinado.'),

(7, 1, 'Em Análise', '2025-02-10', NULL, 'Aguardando agendamento da entrevista virtual com a ONG.'),
(9, 7, 'Em Análise', '2025-02-12', NULL, 'Formulário inicial recebido. Em fase de verificação de documentos.'),
(11, 3, 'Em Análise', '2025-02-14', NULL, 'Avaliando se o adotante possui ambiente adequado para aves.'),
(13, 21, 'Em Análise', '2025-02-15', NULL, 'Visita domiciliar agendada para a próxima semana.'),
(9, 9, 'Em Análise', '2025-02-16', NULL, 'Formulário recebido para adoção de hamster, aguardando fotos do alojamento.'),
(11, 14, 'Em Análise', '2025-02-18', NULL, 'Análise de autorização de órgãos ambientais para posse responsável de papagaio.'),

(14, 4, 'Recusado', '2025-01-15', '2025-01-18', 'Perfil incompatível: presença de animais territoriais no imóvel.'),
(15, 8, 'Recusado', '2025-01-20', '2025-01-23', 'Incompatibilidade com o tipo de residência informado no cadastro.'),
(14, 18, 'Recusado', '2025-02-01', '2025-02-04', 'Falta de tela de proteção adequada em recinto externo.'),

(6, 11, 'Cancelado', '2025-01-08', '2025-01-12', 'Adotante desistiu do processo por motivos de mudança residencial.'),
(8, 20, 'Cancelado', '2025-02-05', '2025-02-09', 'Adotante optou por adiar adoção devido a viagens de trabalho.');

-- Inserção na Tabela apadrinha
INSERT INTO apadrinha (id_adotante, id_animal, tipo_de_contribuicao, valor_recorrente, frequencia, status, data_de_inicio) VALUES
(6, 1, 'Financeiro', 100.00, 'Mensal', 'Ativo', '2025-01-10'),
(6, 3, 'Financeiro', 50.00, 'Mensal', 'Ativo', '2025-02-01'),
(7, 2, 'Financeiro', 75.00, 'Mensal', 'Ativo', '2025-01-15'),
(8, 4, 'Financeiro', 30.00, 'Mensal', 'Ativo', '2025-01-20'),
(9, 6, 'Financeiro', 150.00, 'Mensal', 'Ativo', '2025-02-05'),

(10, 5, 'Ração e Suplementos', 80.00, 'Mensal', 'Ativo', '2025-01-22'),
(11, 8, 'Ração e Medicamentos', 120.00, 'Mensal', 'Ativo', '2025-02-10'),
(12, 10, 'Alimentação Especial', 40.00, 'Mensal', 'Ativo', '2025-01-18'),

(13, 14, 'Financeiro', 200.00, 'Trimestral', 'Ativo', '2025-01-05'),
(14, 19, 'Financeiro', 500.00, 'Anual', 'Ativo', '2025-01-01'),

(15, 21, 'Financeiro', 60.00, 'Mensal', 'Pausado', '2024-11-10'),
(7, 13, 'Cuidados Médicos', 100.00, 'Mensal', 'Encerrado', '2024-08-01'),

(8, 3, 'Alimentação e Frutas', 45.00, 'Mensal', 'Ativo', '2025-02-12'),
(9, 9, 'Insumos e Higiene', 35.00, 'Mensal', 'Ativo', '2025-02-15'),
(10, 18, 'Alimentação Especial', 50.00, 'Mensal', 'Ativo', '2025-01-28'),
(11, 15, 'Cuidados Veterinários', 90.00, 'Mensal', 'Ativo', '2025-02-01'),

(12, 7, 'Financeiro', 80.00, 'Mensal', 'Ativo', '2025-01-10'),
(13, 11, 'Ração e Medicamentos', 110.00, 'Mensal', 'Ativo', '2025-02-03'),
(14, 12, 'Financeiro', 70.00, 'Mensal', 'Ativo', '2025-01-25'),
(15, 16, 'Financeiro', 65.00, 'Mensal', 'Ativo', '2025-02-08'),
(6, 20, 'Vacinas e Cuidados', 85.00, 'Mensal', 'Ativo', '2025-01-30'),
(8, 22, 'Financeiro', 120.00, 'Trimestral', 'Ativo', '2025-02-14');
