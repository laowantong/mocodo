CREATE TABLE PROJET (
  PRIMARY KEY (projet),
  projet  VARCHAR(42) NOT NULL,
  libelle VARCHAR(50)
);

CREATE TABLE TECHNICIEN (
  PRIMARY KEY (technicien),
  technicien     VARCHAR(42) NOT NULL,
  nom_technicien VARCHAR(255)
);

CREATE TABLE UTILISER (
  PRIMARY KEY (carnet, projet),
  carnet     VARCHAR(42) NOT NULL,
  projet     VARCHAR(42) NOT NULL,
  technicien VARCHAR(42) NOT NULL,
  UNIQUE (carnet, technicien),
  UNIQUE (projet, technicien)
);

ALTER TABLE UTILISER ADD FOREIGN KEY (technicien) REFERENCES TECHNICIEN (technicien);
ALTER TABLE UTILISER ADD FOREIGN KEY (projet) REFERENCES PROJET (projet);
