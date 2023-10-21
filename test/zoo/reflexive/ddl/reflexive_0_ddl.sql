CREATE TABLE COMPOSER (
  PRIMARY KEY (piece_composante, piece_composee),
  piece_composante VARCHAR(42) NOT NULL,
  piece_composee   VARCHAR(42) NOT NULL
);

CREATE TABLE HOMME (
  PRIMARY KEY (num_ss),
  num_ss      VARCHAR(8) NOT NULL,
  nom         VARCHAR(255),
  prenom      VARCHAR(255),
  num_ss_pere VARCHAR(8) NULL
);

ALTER TABLE HOMME ADD FOREIGN KEY (num_ss_pere) REFERENCES HOMME (num_ss);
