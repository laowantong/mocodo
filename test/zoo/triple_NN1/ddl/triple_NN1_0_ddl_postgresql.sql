CREATE DATABASE triple_NN1;
\c triple_NN1;

CREATE TABLE GERER (
  ingenieur VARCHAR(42) NOT NULL,
  projet VARCHAR(42) NOT NULL,
  responsable VARCHAR(42) NOT NULL,
  PRIMARY KEY (ingenieur, projet)
);
