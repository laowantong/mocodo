CREATE DATABASE triple_NNN;
\c triple_NNN;

CREATE TABLE APPLIQUER (
  employe VARCHAR(42) NOT NULL,
  projet VARCHAR(42) NOT NULL,
  competence VARCHAR(42) NOT NULL,
  PRIMARY KEY (employe, projet, competence)
);
