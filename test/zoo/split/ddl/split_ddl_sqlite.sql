.open split;

CREATE TABLE BATAILLE (
  nom_bataille VARCHAR(255) NOT NULL,
  lieu VARCHAR(42),
  date DATE,
  PRIMARY KEY (nom_bataille)
);

CREATE TABLE TROPHEE (
  numero VARCHAR(42) NOT NULL,
  type VARCHAR(42),
  etat VARCHAR(42),
  nom_villageois VARCHAR(255) NOT NULL,
  nom_bataille VARCHAR(255) NOT NULL,
  PRIMARY KEY (numero)
  FOREIGN KEY (nom_villageois) REFERENCES VILLAGEOIS (nom_villageois),
  FOREIGN KEY (nom_bataille) REFERENCES BATAILLE (nom_bataille)
);

CREATE TABLE VILLAGEOIS (
  nom_villageois VARCHAR(255) NOT NULL,
  adresse VARCHAR(42),
  fonction VARCHAR(42),
  PRIMARY KEY (nom_villageois)
);
