CREATE TABLE UTILISER (
  PRIMARY KEY (carnet, projet),
  carnet VARCHAR(42) NOT NULL,
  projet VARCHAR(42) NOT NULL,
  technicien VARCHAR(42) NOT NULL,
  CONSTRAINT UTILISER_u1 UNIQUE (carnet, technicien),
  CONSTRAINT UTILISER_u2 UNIQUE (projet, technicien)
);
