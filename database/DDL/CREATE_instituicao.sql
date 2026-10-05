CREATE TABLE instituicao (
    id_usuario INT PRIMARY KEY,
    cnpj VARCHAR(18) UNIQUE,
    razao_social VARCHAR(180),
    selo_verificacao BOOLEAN DEFAULT FALSE,

    CONSTRAINT fk_instituicao 
        FOREIGN KEY (id_usuario) 
        REFERENCES usuario(id_usuario) 
        ON DELETE CASCADE
);
