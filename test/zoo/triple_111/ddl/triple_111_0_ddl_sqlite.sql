.open triple_111;

CREATE TABLE UTILISER (
  carnet VARCHAR(42) NOT NULL,
  projet VARCHAR(42) NOT NULL,
  technicien VARCHAR(42) NOT NULL,
  PRIMARY KEY (carnet, projet)
);

CREATE UNIQUE INDEX UTILISER_u1 ON UTILISER (carnet, technicien);
CREATE UNIQUE INDEX UTILISER_u2 ON UTILISER (projet, technicien);
