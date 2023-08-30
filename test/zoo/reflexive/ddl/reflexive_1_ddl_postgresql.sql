CREATE DATABASE reflexive;
\c reflexive;

CREATE TABLE COMPOSER (
  piece VARCHAR(42),
  piece_1 VARCHAR(42),
  PRIMARY KEY (piece, piece_1)
);

CREATE TABLE HOMME (
  num_ss VARCHAR(8),
  nom VARCHAR(255),
  prenom VARCHAR(255),
  num_ss_1 VARCHAR(8),
  PRIMARY KEY (num_ss)
);

ALTER TABLE HOMME ADD FOREIGN KEY (num_ss_1) REFERENCES HOMME (num_ss);
