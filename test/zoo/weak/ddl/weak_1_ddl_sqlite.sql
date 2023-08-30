.open weak;

CREATE TABLE EXEMPLAIRE (
  oeuvre VARCHAR(42),
  exemplaire VARCHAR(42),
  nb_pages INTEGER,
  date_achat DATE,
  foobar VARCHAR(42),
  PRIMARY KEY (oeuvre, exemplaire)
  FOREIGN KEY (oeuvre) REFERENCES OEUVRE (oeuvre)
);

CREATE TABLE OEUVRE (
  oeuvre VARCHAR(42),
  auteur VARCHAR(42),
  PRIMARY KEY (oeuvre)
);
