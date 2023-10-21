CREATE TABLE TRISTIS (
  PRIMARY KEY (magna),
  magna            VARCHAR(42) NOT NULL,
  vestibulum       VARCHAR(42),
  type             UNSIGNED INT NOT NULL,
  convallis        VARCHAR(42) NULL,
  ipsum            VARCHAR(42) NULL,
  pulvinar         VARCHAR(42) NULL,
  audis            VARCHAR(42) NULL,
  magna_via_mollis VARCHAR(42) NULL,
  magna_via_vitae  VARCHAR(42) NULL,
  tempor           VARCHAR(42) NULL,
  fugit            VARCHAR(42) NULL
);

CREATE TABLE ULTRICES (
  PRIMARY KEY (magna_sodales, magna_lacus),
  magna_sodales VARCHAR(42) NOT NULL,
  magna_lacus   VARCHAR(42) NOT NULL
);

ALTER TABLE TRISTIS ADD FOREIGN KEY (magna_via_vitae) REFERENCES TRISTIS (magna);
ALTER TABLE TRISTIS ADD FOREIGN KEY (magna_via_mollis) REFERENCES TRISTIS (magna);

ALTER TABLE ULTRICES ADD FOREIGN KEY (magna_lacus) REFERENCES TRISTIS (magna);
ALTER TABLE ULTRICES ADD FOREIGN KEY (magna_sodales) REFERENCES TRISTIS (magna);
