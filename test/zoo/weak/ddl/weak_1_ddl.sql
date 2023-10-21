CREATE TABLE EXEMPLAIRE (
  PRIMARY KEY (oeuvre, exemplaire),
  oeuvre     VARCHAR(42) NOT NULL,
  exemplaire VARCHAR(42) NOT NULL,
  nb_pages   INTEGER,
  date_achat DATE,
  foobar     VARCHAR(42)
);

CREATE TABLE OEUVRE (
  PRIMARY KEY (oeuvre),
  oeuvre VARCHAR(42) NOT NULL,
  auteur VARCHAR(42)
);

ALTER TABLE EXEMPLAIRE ADD FOREIGN KEY (oeuvre) REFERENCES OEUVRE (oeuvre);
