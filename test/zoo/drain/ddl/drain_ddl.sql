CREATE TABLE ENTREPRISE (
  PRIMARY KEY (nom_entreprise),
  nom_entreprise VARCHAR(255) NOT NULL,
  adresse        VARCHAR(30),
  telephone      VARCHAR(20)
);

CREATE TABLE ETUDIANT (
  PRIMARY KEY (num_etudiant),
  num_etudiant   VARCHAR(8) NOT NULL,
  nom            VARCHAR(255),
  num_stage      VARCHAR(8) NOT NULL,
  date_signature BINARY(64),
  date           DATE NULL,
  note_stage     TEXT,
  UNIQUE (num_stage)
);

CREATE TABLE STAGE (
  PRIMARY KEY (num_stage),
  num_stage        VARCHAR(8) NOT NULL,
  sujet            VARCHAR(42),
  nom_entreprise   VARCHAR(255) NOT NULL,
  date_proposition DATE
);

ALTER TABLE ETUDIANT ADD FOREIGN KEY (num_stage) REFERENCES STAGE (num_stage);

ALTER TABLE STAGE ADD FOREIGN KEY (nom_entreprise) REFERENCES ENTREPRISE (nom_entreprise);
