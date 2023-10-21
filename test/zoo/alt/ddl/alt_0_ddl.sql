CREATE TABLE CLIENT (
  PRIMARY KEY (ref_client),
  ref_client VARCHAR(8) NOT NULL,
  nom        VARCHAR(255),
  prenom     VARCHAR(255),
  adresse    VARCHAR(30),
  mail       VARCHAR(255),
  UNIQUE (nom, prenom),
  UNIQUE (mail)
);

CREATE TABLE FOO (
  PRIMARY KEY (foo),
  foo  VARCHAR(42) NOT NULL,
  bar  VARCHAR(42),
  biz  VARCHAR(42),
  buz  VARCHAR(42),
  qux  VARCHAR(42),
  quux VARCHAR(42),
  UNIQUE (bar, biz, quux),
  UNIQUE (biz, buz, quux),
  UNIQUE (qux, quux)
);

CREATE TABLE UTILISER (
  PRIMARY KEY (carnet, projet),
  carnet     VARCHAR(42) NOT NULL,
  projet     VARCHAR(42) NOT NULL,
  technicien VARCHAR(42),
  UNIQUE (carnet, technicien),
  UNIQUE (projet, technicien)
);
