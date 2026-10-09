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

CREATE TABLE usuario_telefone (
    id_usuario INT NOT NULL,
    telefone VARCHAR(20) NOT NULL,

    PRIMARY KEY (id_usuario, telefone),

    CONSTRAINT fk_usuario_telefone 
        FOREIGN KEY (id_usuario) 
        REFERENCES usuario(id_usuario) 
        ON DELETE CASCADE
);

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

CREATE TABLE adotante_historico_pets (
    id_historico SERIAL PRIMARY KEY,             
    id_usuario INT NOT NULL,                    
    descricao TEXT NOT NULL,                 
    CONSTRAINT fk_adotante_historico
        FOREIGN KEY (id_usuario)
        REFERENCES adotante(id_usuario)
        ON DELETE CASCADE
);

CREATE TABLE animal (
    id_animal SERIAL PRIMARY KEY,              
    id_instituicao INT NOT NULL,               
    nome VARCHAR(100) NOT NULL,
    especie VARCHAR(80) NOT NULL,             
    raca VARCHAR(80),
    idade INT,
    porte VARCHAR(20),                         
    sexo CHAR(1),                             
    status VARCHAR(30),  
    observacao TEXT,

    CONSTRAINT fk_animal_instituicao 
        FOREIGN KEY (id_instituicao) 
        REFERENCES instituicao(id_usuario)    
        ON DELETE CASCADE
);

CREATE TABLE prontuario_veterinario (      
    id_animal INT NOT NULL,                   
    data_procedimento DATE NOT NULL,
    tipo_procedimento VARCHAR(100) NOT NULL,
    descricao TEXT,

    CONSTRAINT fk_prontuario_animal
        FOREIGN KEY (id_animal)
        REFERENCES animal(id_animal)
        ON DELETE CASCADE,
		
	PRIMARY KEY(id_animal, data_procedimento, tipo_procedimento)
		
);

CREATE TABLE apadrinha (
id_adotante INT NOT NULL,
id_animal INT NOT NULL,
tipo_de_contribuicao VARCHAR(60),
valor_recorrente DECIMAL(10,2),
frequencia VARCHAR(30),
status VARCHAR(30),
data_de_inicio DATE,

	CONSTRAINT fk_apadrinha_adotante
		FOREIGN KEY (id_adotante)
		REFERENCES adotante(id_usuario)
		ON DELETE CASCADE,

	CONSTRAINT fk_apadrinha_animal
		FOREIGN KEY (id_animal)
		REFERENCES animal(id_animal)
		ON DELETE CASCADE,

		PRIMARY KEY (id_adotante, id_animal)
);

CREATE TABLE adota (
id_adotante INT NOT NULL,
id_animal INT NOT NULL,
status VARCHAR(30),
data_de_solicitacao DATE,
data_de_conclusao DATE,
observacao_do_processo TEXT,

CONSTRAINT fk_adota_adotante
		FOREIGN KEY (id_adotante)
		REFERENCES adotante(id_usuario)
		ON DELETE CASCADE,

	CONSTRAINT fk_adota_animal
		FOREIGN KEY (id_animal)
		REFERENCES animal(id_animal)
		ON DELETE CASCADE,

		PRIMARY KEY (id_adotante, id_animal)
);
