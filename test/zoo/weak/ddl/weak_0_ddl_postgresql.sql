CREATE DATABASE weak;
\c weak;

CREATE TABLE EXEMPLAIRE (
  oeuvre VARCHAR(42),
  exemplaire VARCHAR(42),
  foobar VARCHAR(42),
  PRIMARY KEY (oeuvre, exemplaire)
);
