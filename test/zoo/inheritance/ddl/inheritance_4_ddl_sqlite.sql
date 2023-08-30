.open inheritance;

CREATE TABLE LACUS (
  magna VARCHAR(42),
  tempor VARCHAR(42),
  fugit VARCHAR(42),
  PRIMARY KEY (magna)
  FOREIGN KEY (magna) REFERENCES TRISTIS (magna)
);

CREATE TABLE NEC (
  magna VARCHAR(42),
  pulvinar VARCHAR(42),
  audis VARCHAR(42),
  magna_via_mollis VARCHAR(42),
  magna_via_vitae VARCHAR(42),
  PRIMARY KEY (magna)
  FOREIGN KEY (magna) REFERENCES TRISTIS (magna),
  FOREIGN KEY (magna_via_mollis) REFERENCES LACUS (magna),
  FOREIGN KEY (magna_via_vitae) REFERENCES SODALES (magna)
);

CREATE TABLE SODALES (
  magna VARCHAR(42),
  convallis VARCHAR(42),
  ipsum VARCHAR(42),
  PRIMARY KEY (magna)
  FOREIGN KEY (magna) REFERENCES TRISTIS (magna)
);

CREATE TABLE TRISTIS (
  magna VARCHAR(42),
  vestibulum VARCHAR(42),
  type INTEGER,
  PRIMARY KEY (magna)
);

CREATE TABLE ULTRICES (
  magna_sodales VARCHAR(42),
  magna_lacus VARCHAR(42),
  PRIMARY KEY (magna_sodales, magna_lacus)
  FOREIGN KEY (magna_sodales) REFERENCES SODALES (magna),
  FOREIGN KEY (magna_lacus) REFERENCES LACUS (magna)
);
