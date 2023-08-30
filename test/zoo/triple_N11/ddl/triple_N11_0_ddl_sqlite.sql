.open triple_N11;

CREATE TABLE AFFECTER (
  projet VARCHAR(42),
  employe VARCHAR(42),
  site VARCHAR(42),
  PRIMARY KEY (projet, employe)
);

CREATE UNIQUE INDEX AFFECTER_u1 ON AFFECTER (employe, site);
