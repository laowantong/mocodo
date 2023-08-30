CREATE DATABASE reflexive;
\c reflexive;

CREATE TABLE COMPOSER (
  piece_composante VARCHAR(42),
  piece_composee VARCHAR(42),
  PRIMARY KEY (piece_composante, piece_composee)
);

CREATE TABLE HOMME (
  num_ss VARCHAR(8),
  nom VARCHAR(255),
  prenom VARCHAR(255),
  num_ss_pere VARCHAR(8),
  PRIMARY KEY (num_ss)
);

ALTER TABLE HOMME ADD FOREIGN KEY (num_ss_pere) REFERENCES HOMME (num_ss);
