CREATE DATABASE IF NOT EXISTS triple_111;
USE triple_111;

CREATE TABLE PROJET (
  projet VARCHAR(42),
  libelle VARCHAR(50),
  PRIMARY KEY (projet)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE TECHNICIEN (
  technicien VARCHAR(42),
  nom_technicien VARCHAR(255),
  PRIMARY KEY (technicien)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE UTILISER (
  carnet VARCHAR(42),
  projet VARCHAR(42),
  technicien VARCHAR(42),
  PRIMARY KEY (carnet, projet)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

ALTER TABLE UTILISER ADD FOREIGN KEY (technicien) REFERENCES TECHNICIEN (technicien);
ALTER TABLE UTILISER ADD FOREIGN KEY (projet) REFERENCES PROJET (projet);
ALTER TABLE UTILISER ADD CONSTRAINT UTILISER_u1 UNIQUE (carnet, technicien);
ALTER TABLE UTILISER ADD CONSTRAINT UTILISER_u2 UNIQUE (projet, technicien);