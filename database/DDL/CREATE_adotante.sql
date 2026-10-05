CREATE TABLE adotante (
    id_usuario INT PRIMARY KEY,
    nome VARCHAR(150),
    cpf VARCHAR(14) UNIQUE,
    tipo_residencia VARCHAR(60),

    CONSTRAINT fk_adotante 
        FOREIGN KEY (id_usuario) 
        REFERENCES usuario(id_usuario) 
        ON DELETE CASCADE
);
