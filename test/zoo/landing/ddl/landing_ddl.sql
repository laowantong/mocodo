CREATE TABLE AYANT_DROIT (
  PRIMARY KEY (matricule, nom_ayant_droit),
  matricule       VARCHAR(42) NOT NULL,
  nom_ayant_droit VARCHAR(255) NOT NULL,
  lien            VARCHAR(42)
);

CREATE TABLE COMPOSER (
  PRIMARY KEY (ref_piece_composee, ref_piece_composante),
  ref_piece_composee   VARCHAR(8) NOT NULL,
  ref_piece_composante VARCHAR(8) NOT NULL,
  quantite             INTEGER
);

CREATE TABLE DEPARTEMENT (
  PRIMARY KEY (num_departement),
  num_departement VARCHAR(8) NOT NULL,
  nom_departement VARCHAR(255)
);

CREATE TABLE EMPLOYE (
  PRIMARY KEY (matricule),
  matricule       VARCHAR(42) NOT NULL,
  nom_employe     VARCHAR(255),
  num_departement VARCHAR(8) NOT NULL
);

CREATE TABLE FOURNIR (
  PRIMARY KEY (num_projet, ref_piece, num_societe),
  num_projet  VARCHAR(8) NOT NULL,
  ref_piece   VARCHAR(8) NOT NULL,
  num_societe VARCHAR(8) NOT NULL,
  qte_fournie INTEGER
);

CREATE TABLE PIECE (
  PRIMARY KEY (ref_piece),
  ref_piece     VARCHAR(8) NOT NULL,
  libelle_piece VARCHAR(42)
);

CREATE TABLE PROJET (
  PRIMARY KEY (num_projet),
  num_projet            VARCHAR(8) NOT NULL,
  nom_projet            VARCHAR(255),
  matricule_responsable VARCHAR(42) NULL
);

CREATE TABLE REQUERIR (
  PRIMARY KEY (num_projet, ref_piece),
  num_projet  VARCHAR(8) NOT NULL,
  ref_piece   VARCHAR(8) NOT NULL,
  qte_requise INTEGER
);

CREATE TABLE SOCIETE (
  PRIMARY KEY (num_societe),
  num_societe      VARCHAR(8) NOT NULL,
  raison_sociale   VARCHAR(42),
  num_societe_mere VARCHAR(8) NULL
);

CREATE TABLE TRAVAILLER (
  PRIMARY KEY (matricule, num_projet),
  matricule  VARCHAR(42) NOT NULL,
  num_projet VARCHAR(8) NOT NULL
);

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
