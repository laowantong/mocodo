CREATE DATABASE weak;
\c weak;

CREATE TABLE EXEMPLAIRE (
  oeuvre VARCHAR(42) NOT NULL,
  exemplaire VARCHAR(42) NOT NULL,
  foobar VARCHAR(42),
  PRIMARY KEY (oeuvre, exemplaire)
);
