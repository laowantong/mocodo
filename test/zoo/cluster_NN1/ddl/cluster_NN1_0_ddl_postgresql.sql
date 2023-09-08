CREATE DATABASE cluster_NN1;
\c cluster_NN1;

CREATE TABLE RESERVATION (
  num_resa VARCHAR(8),
  arrhes VARCHAR(42),
  date_resa DATE,
  num_voilier VARCHAR(8),
  num_semaine VARCHAR(8),
  tarif VARCHAR(42),
  PRIMARY KEY (num_resa)
);

CREATE TABLE SEMAINE (
  num_semaine VARCHAR(8),
  date_debut DATE,
  PRIMARY KEY (num_semaine)
);

CREATE TABLE VOILIER (
  num_voilier VARCHAR(8),
  longueur DECIMAL(10,2),
  PRIMARY KEY (num_voilier)
);

ALTER TABLE RESERVATION ADD FOREIGN KEY (num_semaine) REFERENCES SEMAINE (num_semaine);
ALTER TABLE RESERVATION ADD FOREIGN KEY (num_voilier) REFERENCES VOILIER (num_voilier);
ALTER TABLE RESERVATION ADD CONSTRAINT RESERVATION_u1 UNIQUE (num_voilier, num_semaine);
ALTER TABLE SEMAINE ADD CONSTRAINT SEMAINE_u1 UNIQUE (date_debut);
