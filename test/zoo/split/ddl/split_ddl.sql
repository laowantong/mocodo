CREATE TABLE BATAILLE (
  PRIMARY KEY (nom_bataille),
  nom_bataille VARCHAR(255) NOT NULL,
  lieu         VARCHAR(42),
  date         DATE
);

CREATE TABLE TROPHEE (
  PRIMARY KEY (numero),
  numero         VARCHAR(8) NOT NULL,
  type           VARCHAR(42),
  etat           VARCHAR(42),
  nom_villageois VARCHAR(255) NOT NULL,
  nom_bataille   VARCHAR(255) NOT NULL
);

CREATE TABLE VILLAGEOIS (
  PRIMARY KEY (nom_villageois),
  nom_villageois VARCHAR(255) NOT NULL,
  adresse        VARCHAR(30),
  fonction       VARCHAR(42)
);

ALTER TABLE TROPHEE ADD FOREIGN KEY (nom_bataille) REFERENCES BATAILLE (nom_bataille);
ALTER TABLE TROPHEE ADD FOREIGN KEY (nom_villageois) REFERENCES VILLAGEOIS (nom_villageois);
