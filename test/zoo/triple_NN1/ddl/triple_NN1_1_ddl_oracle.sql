CREATE TABLE GERER (
  ingenieur VARCHAR(42),
  projet VARCHAR(42),
  responsable VARCHAR(42),
  PRIMARY KEY (ingenieur, projet)
);

CREATE TABLE INGENIEUR (
  ingenieur VARCHAR(42),
  nom_ingenieur VARCHAR(255),
  PRIMARY KEY (ingenieur)
);

CREATE TABLE PROJET (
  projet VARCHAR(42),
  libelle_projet VARCHAR(42),
  PRIMARY KEY (projet)
);

CREATE TABLE RESPONSABLE (
  responsable VARCHAR(42),
  nom_responsable VARCHAR(255),
  PRIMARY KEY (responsable)
);

ALTER TABLE GERER ADD FOREIGN KEY (responsable) REFERENCES RESPONSABLE (responsable);
ALTER TABLE GERER ADD FOREIGN KEY (projet) REFERENCES PROJET (projet);
ALTER TABLE GERER ADD FOREIGN KEY (ingenieur) REFERENCES INGENIEUR (ingenieur);
