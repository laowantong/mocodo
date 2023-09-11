CREATE TABLE EXEMPLAIRE (
  oeuvre VARCHAR(42) NOT NULL,
  exemplaire VARCHAR(42) NOT NULL,
  nb_pages INTEGER,
  date_achat DATE,
  foobar VARCHAR(42),
  PRIMARY KEY (oeuvre, exemplaire)
);

CREATE TABLE OEUVRE (
  oeuvre VARCHAR(42) NOT NULL,
  auteur VARCHAR(42),
  PRIMARY KEY (oeuvre)
);

ALTER TABLE EXEMPLAIRE ADD FOREIGN KEY (oeuvre) REFERENCES OEUVRE (oeuvre);
