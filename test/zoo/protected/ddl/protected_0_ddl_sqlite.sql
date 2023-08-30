.open protected;

CREATE TABLE EROS (
  congue VARCHAR(42),
  PRIMARY KEY (congue)
);

CREATE TABLE LACUS (
  blandit VARCHAR(42),
  elit VARCHAR(42),
  PRIMARY KEY (blandit)
);

CREATE TABLE LIGULA (
  blandit VARCHAR(42),
  congue VARCHAR(42),
  metus VARCHAR(42),
  PRIMARY KEY (blandit)
  FOREIGN KEY (blandit) REFERENCES LACUS (blandit),
  FOREIGN KEY (congue) REFERENCES EROS (congue)
);
