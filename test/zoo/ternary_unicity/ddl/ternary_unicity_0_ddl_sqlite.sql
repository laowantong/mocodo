.open ternary_unicity;

CREATE TABLE DISPONIBILITE (
  semaine VARCHAR(42),
  voilier VARCHAR(42),
  PRIMARY KEY (semaine, voilier)
  FOREIGN KEY (semaine) REFERENCES SEMAINE (semaine)
);

CREATE TABLE RESERVATION (
  id_resa VARCHAR(8),
  num_resa VARCHAR(8),
  arrhes VARCHAR(42),
  date_reservation DATE,
  semaine VARCHAR(42),
  voilier VARCHAR(42),
  PRIMARY KEY (id_resa)
  FOREIGN KEY (semaine, voilier) REFERENCES DISPONIBILITE (semaine, voilier)
);

CREATE TABLE SEMAINE (
  semaine VARCHAR(42),
  date_debut DATE,
  PRIMARY KEY (semaine)
);

CREATE UNIQUE INDEX RESERVATION_u1 ON RESERVATION (num_resa);
CREATE UNIQUE INDEX RESERVATION_u2 ON RESERVATION (semaine, voilier);
CREATE UNIQUE INDEX SEMAINE_u1 ON SEMAINE (date_debut);
