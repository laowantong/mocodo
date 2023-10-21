CREATE TABLE DISPONIBILITE (
  PRIMARY KEY (semaine, voilier),
  semaine VARCHAR(42) NOT NULL,
  voilier VARCHAR(42) NOT NULL
);

CREATE TABLE RESERVATION (
  PRIMARY KEY (id_resa),
  id_resa          VARCHAR(8) NOT NULL,
  num_resa         VARCHAR(8),
  arrhes           VARCHAR(42),
  date_reservation DATE,
  semaine          VARCHAR(42) NOT NULL,
  voilier          VARCHAR(42) NOT NULL,
  UNIQUE (num_resa),
  UNIQUE (semaine, voilier)
);

CREATE TABLE SEMAINE (
  PRIMARY KEY (semaine),
  semaine    VARCHAR(42) NOT NULL,
  date_debut DATE,
  UNIQUE (date_debut)
);

ALTER TABLE DISPONIBILITE ADD FOREIGN KEY (semaine) REFERENCES SEMAINE (semaine);

ALTER TABLE RESERVATION ADD FOREIGN KEY (semaine, voilier) REFERENCES DISPONIBILITE (semaine, voilier);
