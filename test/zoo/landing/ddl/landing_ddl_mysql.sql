CREATE DATABASE IF NOT EXISTS landing;
USE landing;

CREATE TABLE AYANT_DROIT (
  matricule VARCHAR(42),
  nom_ayant_droit VARCHAR(255),
  lien VARCHAR(42),
  PRIMARY KEY (matricule, nom_ayant_droit)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE COMPOSER (
  ref_piece_composee VARCHAR(8),
  ref_piece_composante VARCHAR(8),
  quantite INTEGER,
  PRIMARY KEY (ref_piece_composee, ref_piece_composante)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE DEPARTEMENT (
  num_departement VARCHAR(8),
  nom_departement VARCHAR(255),
  PRIMARY KEY (num_departement)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE EMPLOYE (
  matricule VARCHAR(42),
  nom_employe VARCHAR(255),
  num_departement VARCHAR(8),
  PRIMARY KEY (matricule)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE FOURNIR (
  num_projet VARCHAR(8),
  ref_piece VARCHAR(8),
  num_societe VARCHAR(8),
  qte_fournie INTEGER,
  PRIMARY KEY (num_projet, ref_piece, num_societe)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE PIECE (
  ref_piece VARCHAR(8),
  libelle_piece VARCHAR(42),
  PRIMARY KEY (ref_piece)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE PROJET (
  num_projet VARCHAR(8),
  nom_projet VARCHAR(255),
  matricule_responsable VARCHAR(42),
  PRIMARY KEY (num_projet)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE REQUERIR (
  num_projet VARCHAR(8),
  ref_piece VARCHAR(8),
  qte_requise INTEGER,
  PRIMARY KEY (num_projet, ref_piece)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE SOCIETE (
  num_societe VARCHAR(8),
  raison_sociale VARCHAR(42),
  num_societe_mere VARCHAR(8),
  PRIMARY KEY (num_societe)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE TRAVAILLER (
  matricule VARCHAR(42),
  num_projet VARCHAR(8),
  PRIMARY KEY (matricule, num_projet)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

ALTER TABLE AYANT_DROIT ADD FOREIGN KEY (matricule) REFERENCES EMPLOYE (matricule);
ALTER TABLE COMPOSER ADD FOREIGN KEY (ref_piece_composante) REFERENCES PIECE (ref_piece);
ALTER TABLE COMPOSER ADD FOREIGN KEY (ref_piece_composee) REFERENCES PIECE (ref_piece);
ALTER TABLE EMPLOYE ADD FOREIGN KEY (num_departement) REFERENCES DEPARTEMENT (num_departement);
ALTER TABLE FOURNIR ADD FOREIGN KEY (num_societe) REFERENCES SOCIETE (num_societe);
ALTER TABLE FOURNIR ADD FOREIGN KEY (ref_piece) REFERENCES PIECE (ref_piece);
ALTER TABLE FOURNIR ADD FOREIGN KEY (num_projet) REFERENCES PROJET (num_projet);
ALTER TABLE PROJET ADD FOREIGN KEY (matricule_responsable) REFERENCES EMPLOYE (matricule);
ALTER TABLE REQUERIR ADD FOREIGN KEY (ref_piece) REFERENCES PIECE (ref_piece);
ALTER TABLE REQUERIR ADD FOREIGN KEY (num_projet) REFERENCES PROJET (num_projet);
ALTER TABLE SOCIETE ADD FOREIGN KEY (num_societe_mere) REFERENCES SOCIETE (num_societe);
ALTER TABLE TRAVAILLER ADD FOREIGN KEY (num_projet) REFERENCES PROJET (num_projet);
ALTER TABLE TRAVAILLER ADD FOREIGN KEY (matricule) REFERENCES EMPLOYE (matricule);
