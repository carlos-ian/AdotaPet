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
