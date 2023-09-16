CREATE TABLE APPLIQUER (
  PRIMARY KEY (employe, projet, competence),
  employe VARCHAR(42) NOT NULL,
  projet VARCHAR(42) NOT NULL,
  competence VARCHAR(42) NOT NULL
);

CREATE TABLE COMPETENCE (
  PRIMARY KEY (competence),
  competence VARCHAR(42) NOT NULL,
  libelle VARCHAR(50)
);

CREATE TABLE EMPLOYE (
  PRIMARY KEY (employe),
  employe VARCHAR(42) NOT NULL,
  nom VARCHAR(255)
);

CREATE TABLE PROJET (
  PRIMARY KEY (projet),
  projet VARCHAR(42) NOT NULL,
  date_debut DATE,
  date_fin DATE
);

ALTER TABLE APPLIQUER ADD FOREIGN KEY (competence) REFERENCES COMPETENCE (competence);
ALTER TABLE APPLIQUER ADD FOREIGN KEY (projet) REFERENCES PROJET (projet);
ALTER TABLE APPLIQUER ADD FOREIGN KEY (employe) REFERENCES EMPLOYE (employe);