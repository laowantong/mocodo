CREATE TABLE UTILISER (
  PRIMARY KEY (carnet, projet),
  carnet     VARCHAR(42) NOT NULL,
  projet     VARCHAR(42) NOT NULL,
  technicien VARCHAR(42) NOT NULL,
  UNIQUE (carnet, technicien),
  UNIQUE (projet, technicien)
);
