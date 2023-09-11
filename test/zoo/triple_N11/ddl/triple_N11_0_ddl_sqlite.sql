.open triple_N11;

CREATE TABLE AFFECTER (
  projet VARCHAR(42) NOT NULL,
  employe VARCHAR(42) NOT NULL,
  site VARCHAR(42) NOT NULL,
  PRIMARY KEY (projet, employe)
);

CREATE UNIQUE INDEX AFFECTER_u1 ON AFFECTER (employe, site);
