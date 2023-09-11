.open inheritance;

CREATE TABLE TRISTIS (
  magna VARCHAR(42) NOT NULL,
  vestibulum VARCHAR(42),
  type INTEGER,
  convallis VARCHAR(42) NULL,
  ipsum VARCHAR(42) NULL,
  pulvinar VARCHAR(42) NULL,
  audis VARCHAR(42) NULL,
  magna_via_mollis VARCHAR(42) NULL,
  magna_via_vitae VARCHAR(42) NULL,
  tempor VARCHAR(42) NULL,
  fugit VARCHAR(42) NULL,
  PRIMARY KEY (magna)
  FOREIGN KEY (magna_via_mollis) REFERENCES TRISTIS (magna),
  FOREIGN KEY (magna_via_vitae) REFERENCES TRISTIS (magna)
);

CREATE TABLE ULTRICES (
  magna_sodales VARCHAR(42) NOT NULL,
  magna_lacus VARCHAR(42) NOT NULL,
  PRIMARY KEY (magna_sodales, magna_lacus)
  FOREIGN KEY (magna_sodales) REFERENCES TRISTIS (magna),
  FOREIGN KEY (magna_lacus) REFERENCES TRISTIS (magna)
);
