.open triple_NN1;

CREATE TABLE GERER (
  ingenieur VARCHAR(42) NOT NULL,
  projet VARCHAR(42) NOT NULL,
  responsable VARCHAR(42) NOT NULL,
  PRIMARY KEY (ingenieur, projet)
  FOREIGN KEY (ingenieur) REFERENCES INGENIEUR (ingenieur),
  FOREIGN KEY (projet) REFERENCES PROJET (projet),
  FOREIGN KEY (responsable) REFERENCES RESPONSABLE (responsable)
);

CREATE TABLE INGENIEUR (
  ingenieur VARCHAR(42) NOT NULL,
  nom_ingenieur VARCHAR(255),
  PRIMARY KEY (ingenieur)
);

CREATE TABLE PROJET (
  projet VARCHAR(42) NOT NULL,
  libelle_projet VARCHAR(42),
  PRIMARY KEY (projet)
);

CREATE TABLE RESPONSABLE (
  responsable VARCHAR(42) NOT NULL,
  nom_responsable VARCHAR(255),
  PRIMARY KEY (responsable)
);
