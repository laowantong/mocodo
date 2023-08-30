CREATE DATABASE triple_NN1;
\c triple_NN1;

CREATE TABLE GERER (
  ingenieur VARCHAR(42),
  projet VARCHAR(42),
  responsable VARCHAR(42),
  PRIMARY KEY (ingenieur, projet)
);
