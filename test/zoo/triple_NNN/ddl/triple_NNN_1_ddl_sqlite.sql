.open triple_NNN;

CREATE TABLE APPLIQUER (
  employe VARCHAR(42),
  projet VARCHAR(42),
  competence VARCHAR(42),
  PRIMARY KEY (employe, projet, competence)
  FOREIGN KEY (employe) REFERENCES EMPLOYE (employe),
  FOREIGN KEY (projet) REFERENCES PROJET (projet),
  FOREIGN KEY (competence) REFERENCES COMPETENCE (competence)
);

CREATE TABLE COMPETENCE (
  competence VARCHAR(42),
  libelle VARCHAR(50),
  PRIMARY KEY (competence)
);

CREATE TABLE EMPLOYE (
  employe VARCHAR(42),
  nom VARCHAR(255),
  PRIMARY KEY (employe)
);

CREATE TABLE PROJET (
  projet VARCHAR(42),
  date_debut DATE,
  date_fin DATE,
  PRIMARY KEY (projet)
);
