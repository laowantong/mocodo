.open cluster_NN1;

CREATE TABLE RESERVATION (
  num_resa VARCHAR(8) NOT NULL,
  arrhes VARCHAR(42),
  date_resa DATE,
  num_voilier VARCHAR(8) NOT NULL,
  num_semaine VARCHAR(8) NOT NULL,
  tarif VARCHAR(42),
  PRIMARY KEY (num_resa)
  FOREIGN KEY (num_voilier) REFERENCES VOILIER (num_voilier),
  FOREIGN KEY (num_semaine) REFERENCES SEMAINE (num_semaine)
);

CREATE TABLE SEMAINE (
  num_semaine VARCHAR(8) NOT NULL,
  date_debut DATE,
  PRIMARY KEY (num_semaine)
);

CREATE TABLE VOILIER (
  num_voilier VARCHAR(8) NOT NULL,
  longueur DECIMAL(10,2),
  PRIMARY KEY (num_voilier)
);

CREATE UNIQUE INDEX RESERVATION_u1 ON RESERVATION (num_voilier, num_semaine);
CREATE UNIQUE INDEX SEMAINE_u1 ON SEMAINE (date_debut);
