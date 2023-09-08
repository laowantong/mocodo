.open landing;

CREATE TABLE AYANT_DROIT (
  matricule VARCHAR(42),
  nom_ayant_droit VARCHAR(255),
  lien VARCHAR(42),
  PRIMARY KEY (matricule, nom_ayant_droit)
  FOREIGN KEY (matricule) REFERENCES EMPLOYE (matricule)
);

CREATE TABLE COMPOSER (
  ref_piece_composee VARCHAR(8),
  ref_piece_composante VARCHAR(8),
  quantite INTEGER,
  PRIMARY KEY (ref_piece_composee, ref_piece_composante)
  FOREIGN KEY (ref_piece_composee) REFERENCES PIECE (ref_piece),
  FOREIGN KEY (ref_piece_composante) REFERENCES PIECE (ref_piece)
);

CREATE TABLE DEPARTEMENT (
  num_departement VARCHAR(8),
  nom_departement VARCHAR(255),
  PRIMARY KEY (num_departement)
);

CREATE TABLE EMPLOYE (
  matricule VARCHAR(42),
  nom_employe VARCHAR(255),
  num_departement VARCHAR(8),
  PRIMARY KEY (matricule)
  FOREIGN KEY (num_departement) REFERENCES DEPARTEMENT (num_departement)
);

CREATE TABLE FOURNIR (
  num_projet VARCHAR(8),
  ref_piece VARCHAR(8),
  num_societe VARCHAR(8),
  qte_fournie INTEGER,
  PRIMARY KEY (num_projet, ref_piece, num_societe)
  FOREIGN KEY (num_projet) REFERENCES PROJET (num_projet),
  FOREIGN KEY (ref_piece) REFERENCES PIECE (ref_piece),
  FOREIGN KEY (num_societe) REFERENCES SOCIETE (num_societe)
);

CREATE TABLE PIECE (
  ref_piece VARCHAR(8),
  libelle_piece VARCHAR(42),
  PRIMARY KEY (ref_piece)
);

CREATE TABLE PROJET (
  num_projet VARCHAR(8),
  nom_projet VARCHAR(255),
  matricule_responsable VARCHAR(42),
  PRIMARY KEY (num_projet)
  FOREIGN KEY (matricule_responsable) REFERENCES EMPLOYE (matricule)
);

CREATE TABLE REQUERIR (
  num_projet VARCHAR(8),
  ref_piece VARCHAR(8),
  qte_requise INTEGER,
  PRIMARY KEY (num_projet, ref_piece)
  FOREIGN KEY (num_projet) REFERENCES PROJET (num_projet),
  FOREIGN KEY (ref_piece) REFERENCES PIECE (ref_piece)
);

CREATE TABLE SOCIETE (
  num_societe VARCHAR(8),
  raison_sociale VARCHAR(42),
  num_societe_mere VARCHAR(8),
  PRIMARY KEY (num_societe)
  FOREIGN KEY (num_societe_mere) REFERENCES SOCIETE (num_societe)
);

CREATE TABLE TRAVAILLER (
  matricule VARCHAR(42),
  num_projet VARCHAR(8),
  PRIMARY KEY (matricule, num_projet)
  FOREIGN KEY (matricule) REFERENCES EMPLOYE (matricule),
  FOREIGN KEY (num_projet) REFERENCES PROJET (num_projet)
);
