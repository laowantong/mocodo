-- Generated by Mocodo 4.0.3

CREATE TABLE AFFECTER (
  PRIMARY KEY (projet, employe),
  projet VARCHAR(42) NOT NULL,
  employe VARCHAR(42) NOT NULL,
  site VARCHAR(42) NOT NULL,
  UNIQUE (employe, site)
);

CREATE TABLE EMPLOYE (
  PRIMARY KEY (employe),
  employe VARCHAR(42) NOT NULL,
  nom_employe VARCHAR(255)
);

CREATE TABLE PROJET (
  PRIMARY KEY (projet),
  projet VARCHAR(42) NOT NULL,
  libelle VARCHAR(50)
);

CREATE TABLE SITE (
  PRIMARY KEY (site),
  site VARCHAR(42) NOT NULL,
  position POINT
);

ALTER TABLE AFFECTER ADD FOREIGN KEY (site) REFERENCES SITE (site);
ALTER TABLE AFFECTER ADD FOREIGN KEY (employe) REFERENCES EMPLOYE (employe);
ALTER TABLE AFFECTER ADD FOREIGN KEY (projet) REFERENCES PROJET (projet);
