.open triple_111;

CREATE TABLE PROJET (
  projet VARCHAR(42) NOT NULL,
  libelle VARCHAR(50),
  PRIMARY KEY (projet)
);

CREATE TABLE TECHNICIEN (
  technicien VARCHAR(42) NOT NULL,
  nom_technicien VARCHAR(255),
  PRIMARY KEY (technicien)
);

CREATE TABLE UTILISER (
  carnet VARCHAR(42) NOT NULL,
  projet VARCHAR(42) NOT NULL,
  technicien VARCHAR(42) NOT NULL,
  PRIMARY KEY (carnet, projet)
  FOREIGN KEY (projet) REFERENCES PROJET (projet),
  FOREIGN KEY (technicien) REFERENCES TECHNICIEN (technicien)
);

CREATE UNIQUE INDEX UTILISER_u1 ON UTILISER (carnet, technicien);
CREATE UNIQUE INDEX UTILISER_u2 ON UTILISER (projet, technicien);
