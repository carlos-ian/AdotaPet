CREATE TABLE usuario (
    id_usuario SERIAL PRIMARY KEY,
    email VARCHAR(150) UNIQUE NOT NULL,
    senha VARCHAR(255) NOT NULL,
    rua VARCHAR(120),
    numero VARCHAR(20),
    bairro VARCHAR(100),
    cep VARCHAR(10),
    cidade VARCHAR(100),
    estado CHAR(2),
    complemento VARCHAR(120),
    tipo_usuario VARCHAR(30) NOT NULL
);
