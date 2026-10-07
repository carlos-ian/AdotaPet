INSERT INTO apadrinha (id_adotante, id_animal, tipo_de_contribuicao, valor_recorrente, frequencia, status, data_de_inicio) VALUES
-- Apadrinhamentos Financeiros Recorrentes
(6, 1, 'Financeiro', 100.00, 'Mensal', 'Ativo', '2025-01-10'),
(6, 3, 'Financeiro', 50.00, 'Mensal', 'Ativo', '2025-02-01'),
(7, 2, 'Financeiro', 75.00, 'Mensal', 'Ativo', '2025-01-15'),
(8, 4, 'Financeiro', 30.00, 'Mensal', 'Ativo', '2025-01-20'),
(9, 6, 'Financeiro', 150.00, 'Mensal', 'Ativo', '2025-02-05'),

-- Apadrinhamentos de Ração e Insumos
(10, 5, 'Ração e Suplementos', 80.00, 'Mensal', 'Ativo', '2025-01-22'),
(11, 8, 'Ração e Medicamentos', 120.00, 'Mensal', 'Ativo', '2025-02-10'),
(12, 10, 'Alimentação Especial', 40.00, 'Mensal', 'Ativo', '2025-01-18'),

-- Apadrinhamentos Trimestrais ou Anuais
(13, 14, 'Financeiro', 200.00, 'Trimestral', 'Ativo', '2025-01-05'),
(14, 19, 'Financeiro', 500.00, 'Anual', 'Ativo', '2025-01-01'),

-- Apadrinhamentos Encerrados ou Pausados
(15, 21, 'Financeiro', 60.00, 'Mensal', 'Pausado', '2024-11-10'),
(7, 13, 'Cuidados Médicos', 100.00, 'Mensal', 'Encerrado', '2024-08-01'),

-- Apadrinhamentos Adicionais (Aves e Pequenos Animais)
(8, 3, 'Alimentação e Frutas', 45.00, 'Mensal', 'Ativo', '2025-02-12'),
(9, 9, 'Insumos e Higiene', 35.00, 'Mensal', 'Ativo', '2025-02-15'),
(10, 18, 'Alimentação Especial', 50.00, 'Mensal', 'Ativo', '2025-01-28'),
(11, 15, 'Cuidados Veterinários', 90.00, 'Mensal', 'Ativo', '2025-02-01'),

-- Apadrinhamentos Adicionais (Cães e Gatos)
(12, 7, 'Financeiro', 80.00, 'Mensal', 'Ativo', '2025-01-10'),
(13, 11, 'Ração e Medicamentos', 110.00, 'Mensal', 'Ativo', '2025-02-03'),
(14, 12, 'Financeiro', 70.00, 'Mensal', 'Ativo', '2025-01-25'),
(15, 16, 'Financeiro', 65.00, 'Mensal', 'Ativo', '2025-02-08'),
(6, 20, 'Vacinas e Cuidados', 85.00, 'Mensal', 'Ativo', '2025-01-30'),
(8, 22, 'Financeiro', 120.00, 'Trimestral', 'Ativo', '2025-02-14');