CREATE TABLE adotante_historico_pets (
    id_historico SERIAL PRIMARY KEY,             
    id_usuario INT NOT NULL,                    
    descricao TEXT NOT NULL,                 
    CONSTRAINT fk_adotante_historico
        FOREIGN KEY (id_usuario)
        REFERENCES adotante(id_usuario)
        ON DELETE CASCADE
);
