CREATE TABLE CLIENT (
  PRIMARY KEY (ref_client),
  ref_client VARCHAR(8) NOT NULL,
  nom VARCHAR(255),
  prenom VARCHAR(255),
  adresse VARCHAR(42),
  mail VARCHAR(255),
  CONSTRAINT CLIENT_u1 UNIQUE (nom, prenom),
  CONSTRAINT CLIENT_u2 UNIQUE (mail)
);

CREATE TABLE FOO (
  PRIMARY KEY (foo),
  foo VARCHAR(42) NOT NULL,
  bar VARCHAR(42),
  biz VARCHAR(42),
  buz VARCHAR(42),
  qux VARCHAR(42),
  quux VARCHAR(42),
  CONSTRAINT FOO_u1 UNIQUE (bar, biz, quux),
  CONSTRAINT FOO_u2 UNIQUE (biz, buz, quux),
  CONSTRAINT FOO_u3 UNIQUE (qux, quux)
);

CREATE TABLE UTILISER (
  PRIMARY KEY (carnet, projet),
  carnet VARCHAR(42) NOT NULL,
  projet VARCHAR(42) NOT NULL,
  technicien VARCHAR(42),
  CONSTRAINT UTILISER_u1 UNIQUE (carnet, technicien),
  CONSTRAINT UTILISER_u2 UNIQUE (projet, technicien)
);
