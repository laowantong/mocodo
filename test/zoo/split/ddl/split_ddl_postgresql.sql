CREATE DATABASE split;
\c split;

CREATE TABLE BATAILLE (
  nom_bataille VARCHAR(255),
  lieu VARCHAR(42),
  date DATE,
  PRIMARY KEY (nom_bataille)
);

CREATE TABLE TROPHEE (
  numero VARCHAR(42),
  type VARCHAR(42),
  etat VARCHAR(42),
  nom_villageois VARCHAR(255),
  nom_bataille VARCHAR(255),
  PRIMARY KEY (numero)
);

CREATE TABLE VILLAGEOIS (
  nom_villageois VARCHAR(255),
  adresse VARCHAR(42),
  fonction VARCHAR(42),
  PRIMARY KEY (nom_villageois)
);

ALTER TABLE TROPHEE ADD FOREIGN KEY (nom_bataille) REFERENCES BATAILLE (nom_bataille);
ALTER TABLE TROPHEE ADD FOREIGN KEY (nom_villageois) REFERENCES VILLAGEOIS (nom_villageois);