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
