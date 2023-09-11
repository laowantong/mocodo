.open inheritance;

CREATE TABLE ALIQUET (
  magna VARCHAR(42) NOT NULL,
  tellus VARCHAR(42) NOT NULL,
  type INTEGER NOT NULL,
  PRIMARY KEY (magna, tellus)
  FOREIGN KEY (tellus) REFERENCES DIGNISSIM (tellus)
);

CREATE TABLE CONSEQUAT (
  fermentum VARCHAR(42) NOT NULL,
  dederit VARCHAR(42),
  PRIMARY KEY (fermentum)
);

CREATE TABLE CURABITUR (
  gravida VARCHAR(42) NOT NULL,
  amor VARCHAR(42),
  PRIMARY KEY (gravida)
);

CREATE TABLE DIGNISSIM (
  tellus VARCHAR(42) NOT NULL,
  terra VARCHAR(42),
  PRIMARY KEY (tellus)
);

CREATE TABLE LACUS (
  magna VARCHAR(42) NOT NULL,
  vestibulum VARCHAR(42),
  fermentum VARCHAR(42) NOT NULL,
  tempor VARCHAR(42),
  fugit VARCHAR(42),
  PRIMARY KEY (magna)
  FOREIGN KEY (fermentum) REFERENCES CONSEQUAT (fermentum)
);

CREATE TABLE LIBERO (
  posuere VARCHAR(42) NOT NULL,
  lacrima VARCHAR(42),
  PRIMARY KEY (posuere)
);

CREATE TABLE NEC (
  magna VARCHAR(42) NOT NULL,
  vestibulum VARCHAR(42),
  fermentum VARCHAR(42) NOT NULL,
  pulvinar VARCHAR(42),
  audis VARCHAR(42),
  gravida VARCHAR(42) NOT NULL,
  PRIMARY KEY (magna)
  FOREIGN KEY (fermentum) REFERENCES CONSEQUAT (fermentum),
  FOREIGN KEY (gravida) REFERENCES CURABITUR (gravida)
);

CREATE TABLE QUAM (
  cras VARCHAR(42) NOT NULL,
  sed VARCHAR(42),
  magna VARCHAR(42) NOT NULL,
  PRIMARY KEY (cras)
  FOREIGN KEY (magna) REFERENCES SODALES (magna)
);

CREATE TABLE SODALES (
  magna VARCHAR(42) NOT NULL,
  vestibulum VARCHAR(42),
  fermentum VARCHAR(42) NOT NULL,
  convallis VARCHAR(42),
  ipsum VARCHAR(42),
  PRIMARY KEY (magna)
  FOREIGN KEY (fermentum) REFERENCES CONSEQUAT (fermentum)
);

CREATE TABLE SUSCIPIT (
  orci VARCHAR(42) NOT NULL,
  lorem VARCHAR(42),
  magna VARCHAR(42) NOT NULL,
  type INTEGER NOT NULL,
  PRIMARY KEY (orci)
);

CREATE TABLE ULTRICES (
  posuere VARCHAR(42) NOT NULL,
  magna VARCHAR(42) NOT NULL,
  PRIMARY KEY (posuere, magna)
  FOREIGN KEY (posuere) REFERENCES LIBERO (posuere),
  FOREIGN KEY (magna) REFERENCES LACUS (magna)
);
