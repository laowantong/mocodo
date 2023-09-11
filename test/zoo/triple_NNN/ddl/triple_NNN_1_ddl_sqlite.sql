.open triple_NNN;

CREATE TABLE APPLIQUER (
  employe VARCHAR(42) NOT NULL,
  projet VARCHAR(42) NOT NULL,
  competence VARCHAR(42) NOT NULL,
  PRIMARY KEY (employe, projet, competence)
  FOREIGN KEY (employe) REFERENCES EMPLOYE (employe),
  FOREIGN KEY (projet) REFERENCES PROJET (projet),
  FOREIGN KEY (competence) REFERENCES COMPETENCE (competence)
);

CREATE TABLE COMPETENCE (
  competence VARCHAR(42) NOT NULL,
  libelle VARCHAR(50),
  PRIMARY KEY (competence)
);

CREATE TABLE EMPLOYE (
  employe VARCHAR(42) NOT NULL,
  nom VARCHAR(255),
  PRIMARY KEY (employe)
);

CREATE TABLE PROJET (
  projet VARCHAR(42) NOT NULL,
  date_debut DATE,
  date_fin DATE,
  PRIMARY KEY (projet)
);
