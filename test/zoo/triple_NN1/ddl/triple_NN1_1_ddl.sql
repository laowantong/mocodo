CREATE TABLE GERER (
  PRIMARY KEY (ingenieur, projet),
  ingenieur   VARCHAR(42) NOT NULL,
  projet      VARCHAR(42) NOT NULL,
  responsable VARCHAR(42) NOT NULL
);

CREATE TABLE INGENIEUR (
  PRIMARY KEY (ingenieur),
  ingenieur     VARCHAR(42) NOT NULL,
  nom_ingenieur VARCHAR(255)
);

CREATE TABLE PROJET (
  PRIMARY KEY (projet),
  projet         VARCHAR(42) NOT NULL,
  libelle_projet VARCHAR(42)
);

CREATE TABLE RESPONSABLE (
  PRIMARY KEY (responsable),
  responsable     VARCHAR(42) NOT NULL,
  nom_responsable VARCHAR(255)
);

ALTER TABLE GERER ADD FOREIGN KEY (responsable) REFERENCES RESPONSABLE (responsable);
ALTER TABLE GERER ADD FOREIGN KEY (projet) REFERENCES PROJET (projet);
ALTER TABLE GERER ADD FOREIGN KEY (ingenieur) REFERENCES INGENIEUR (ingenieur);
