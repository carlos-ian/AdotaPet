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
