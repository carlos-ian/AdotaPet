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
