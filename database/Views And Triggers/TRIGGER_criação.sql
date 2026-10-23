-- Trigger para a tabela 'animal'
CREATE TRIGGER trg_auditoria_animal
BEFORE INSERT OR UPDATE ON animal
FOR EACH ROW
EXECUTE FUNCTION fn_atualiza_datas_auditoria();

-- Trigger para a tabela 'adota'
CREATE TRIGGER trg_auditoria_adota
BEFORE INSERT OR UPDATE ON adota
FOR EACH ROW
EXECUTE FUNCTION fn_atualiza_datas_auditoria();