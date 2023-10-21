CREATE TABLE AFFECTER (
  PRIMARY KEY (projet, employe),
  projet  VARCHAR(42) NOT NULL,
  employe VARCHAR(42) NOT NULL,
  site    VARCHAR(42) NOT NULL,
  UNIQUE (employe, site)
);
