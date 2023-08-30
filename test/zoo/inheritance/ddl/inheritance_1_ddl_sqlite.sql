.open inheritance;

CREATE TABLE ALIQUET (
  magna VARCHAR(42),
  tellus VARCHAR(42),
  PRIMARY KEY (magna, tellus)
  FOREIGN KEY (magna) REFERENCES TRISTIS (magna),
  FOREIGN KEY (tellus) REFERENCES DIGNISSIM (tellus)
);

CREATE TABLE CONSEQUAT (
  fermentum VARCHAR(42),
  dederit VARCHAR(42),
  PRIMARY KEY (fermentum)
);

CREATE TABLE CURABITUR (
  gravida VARCHAR(42),
  amor VARCHAR(42),
  PRIMARY KEY (gravida)
);

CREATE TABLE DIGNISSIM (
  tellus VARCHAR(42),
  terra VARCHAR(42),
  PRIMARY KEY (tellus)
);

CREATE TABLE LACUS (
  magna VARCHAR(42),
  tempor VARCHAR(42),
  fugit VARCHAR(42),
  PRIMARY KEY (magna)
  FOREIGN KEY (magna) REFERENCES TRISTIS (magna)
);

CREATE TABLE LIBERO (
  posuere VARCHAR(42),
  lacrima VARCHAR(42),
  PRIMARY KEY (posuere)
);

CREATE TABLE NEC (
  magna VARCHAR(42),
  pulvinar VARCHAR(42),
  audis VARCHAR(42),
  gravida VARCHAR(42),
  PRIMARY KEY (magna)
  FOREIGN KEY (magna) REFERENCES TRISTIS (magna),
  FOREIGN KEY (gravida) REFERENCES CURABITUR (gravida)
);

CREATE TABLE QUAM (
  cras VARCHAR(42),
  sed VARCHAR(42),
  magna VARCHAR(42),
  PRIMARY KEY (cras)
  FOREIGN KEY (magna) REFERENCES SODALES (magna)
);

CREATE TABLE SODALES (
  magna VARCHAR(42),
  convallis VARCHAR(42),
  ipsum VARCHAR(42),
  PRIMARY KEY (magna)
  FOREIGN KEY (magna) REFERENCES TRISTIS (magna)
);

CREATE TABLE SUSCIPIT (
  orci VARCHAR(42),
  lorem VARCHAR(42),
  magna VARCHAR(42),
  PRIMARY KEY (orci)
  FOREIGN KEY (magna) REFERENCES TRISTIS (magna)
);

CREATE TABLE TRISTIS (
  magna VARCHAR(42),
  vestibulum VARCHAR(42),
  fermentum VARCHAR(42),
  type INTEGER,
  PRIMARY KEY (magna)
  FOREIGN KEY (fermentum) REFERENCES CONSEQUAT (fermentum)
);

CREATE TABLE ULTRICES (
  posuere VARCHAR(42),
  magna VARCHAR(42),
  PRIMARY KEY (posuere, magna)
  FOREIGN KEY (posuere) REFERENCES LIBERO (posuere),
  FOREIGN KEY (magna) REFERENCES LACUS (magna)
);
