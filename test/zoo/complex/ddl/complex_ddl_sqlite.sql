.open complex;

CREATE TABLE ANIMAL (
  code_espece VARCHAR(8) NOT NULL,
  nom VARCHAR(255) NOT NULL,
  date_naissance DATE NOT NULL,
  sexe CHAR(1),
  date_deces DATE,
  code_espece_mere VARCHAR(8) NULL,
  nom_mere VARCHAR(255) NULL,
  date_naissance_mere DATE NULL,
  type_alimentation INTEGER NOT NULL,
  CARNIVORE INTEGER NOT NULL,
  quantite_viande INTEGER NULL,
  HERBIVORE INTEGER NOT NULL,
  plante_preferee VARCHAR(42) NULL,
  PRIMARY KEY (code_espece, nom, date_naissance)
  FOREIGN KEY (code_espece) REFERENCES ESPECE (code_espece),
  FOREIGN KEY (code_espece_mere, nom_mere, date_naissance_mere) REFERENCES ANIMAL (code_espece, nom, date_naissance)
);

CREATE TABLE ESPECE (
  code_espece VARCHAR(8) NOT NULL,
  nom_latin VARCHAR(255),
  nom_vernaculaire VARCHAR(255),
  PRIMARY KEY (code_espece)
);

CREATE TABLE OCCUPE (
  code_espece VARCHAR(8) NOT NULL,
  nom VARCHAR(255) NOT NULL,
  date_naissance DATE NOT NULL,
  num_enclos VARCHAR(8) NOT NULL,
  date_debut DATE NOT NULL,
  date_fin DATE NOT NULL,
  PRIMARY KEY (code_espece, nom, date_naissance, num_enclos)
  FOREIGN KEY (code_espece, nom, date_naissance) REFERENCES ANIMAL (code_espece, nom, date_naissance)
);

CREATE TABLE PEUT_COHABITER_AVEC (
  code_espece VARCHAR(8) NOT NULL,
  code_espece_commensale VARCHAR(8) NOT NULL,
  nb_max_commensaux INTEGER,
  PRIMARY KEY (code_espece, code_espece_commensale)
  FOREIGN KEY (code_espece) REFERENCES ESPECE (code_espece),
  FOREIGN KEY (code_espece_commensale) REFERENCES ESPECE (code_espece)
);

CREATE TABLE PEUT_VIVRE_DANS (
  code_espece VARCHAR(8) NOT NULL,
  num_enclos VARCHAR(8) NOT NULL,
  nb_max_congeneres INTEGER,
  PRIMARY KEY (code_espece, num_enclos)
  FOREIGN KEY (code_espece) REFERENCES ESPECE (code_espece)
);

CREATE UNIQUE INDEX ESPECE_u1 ON ESPECE (nom_latin);
