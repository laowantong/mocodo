CREATE DATABASE triple_NNN;
\c triple_NNN;

CREATE TABLE APPLIQUER (
  employe VARCHAR(42),
  projet VARCHAR(42),
  competence VARCHAR(42),
  PRIMARY KEY (employe, projet, competence)
);