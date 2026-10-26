-- Adiciona os campos na tabela animal
ALTER TABLE animal 
ADD COLUMN data_inclusao TIMESTAMP,
ADD COLUMN data_alteracao TIMESTAMP;

-- Adiciona os campos na tabela adota
ALTER TABLE adota 
ADD COLUMN data_inclusao TIMESTAMP,
ADD COLUMN data_alteracao TIMESTAMP;

CREATE OR REPLACE FUNCTION fn_atualiza_datas_auditoria()
RETURNS TRIGGER AS $$
BEGIN
    IF (TG_OP = 'INSERT') THEN
        NEW.data_inclusao := NOW();
        NEW.data_alteracao := NULL; -- Inicia nulo pois ainda não houve alteração
    ELSIF (TG_OP = 'UPDATE') THEN
        NEW.data_inclusao := OLD.data_inclusao; -- Preserva a data original de criação
        NEW.data_alteracao := NOW(); -- Atualiza a data de alteração
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;
