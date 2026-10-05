CREATE TABLE usuario_telefone (
    id_usuario INT NOT NULL,
    telefone VARCHAR(20) NOT NULL,

    PRIMARY KEY (id_usuario, telefone),

    CONSTRAINT fk_usuario_telefone 
        FOREIGN KEY (id_usuario) 
        REFERENCES usuario(id_usuario) 
        ON DELETE CASCADE
);
