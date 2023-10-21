CREATE TABLE RESERVATION (
  PRIMARY KEY (num_resa),
  num_resa    VARCHAR(8) NOT NULL,
  arrhes      VARCHAR(42),
  date_resa   DATE,
  num_voilier VARCHAR(8) NOT NULL,
  num_semaine VARCHAR(8) NOT NULL,
  tarif       VARCHAR(42),
  UNIQUE (num_voilier, num_semaine)
);

CREATE TABLE SEMAINE (
  PRIMARY KEY (num_semaine),
  num_semaine VARCHAR(8) NOT NULL,
  date_debut  DATE,
  UNIQUE (date_debut)
);

CREATE TABLE VOILIER (
  PRIMARY KEY (num_voilier),
  num_voilier VARCHAR(8) NOT NULL,
  longueur    DECIMAL(10,2)
);

ALTER TABLE RESERVATION ADD FOREIGN KEY (num_semaine) REFERENCES SEMAINE (num_semaine);
ALTER TABLE RESERVATION ADD FOREIGN KEY (num_voilier) REFERENCES VOILIER (num_voilier);
