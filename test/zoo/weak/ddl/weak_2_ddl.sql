CREATE TABLE APPARTEMENT (
  PRIMARY KEY (code_rue, num_immeuble, num_etage, num_appart),
  code_rue     VARCHAR(8) NOT NULL,
  num_immeuble VARCHAR(8) NOT NULL,
  num_etage    VARCHAR(8) NOT NULL,
  num_appart   VARCHAR(8) NOT NULL,
  nb_pieces    INTEGER
);

CREATE TABLE ETAGE (
  PRIMARY KEY (code_rue, num_immeuble, num_etage),
  code_rue        VARCHAR(8) NOT NULL,
  num_immeuble    VARCHAR(8) NOT NULL,
  num_etage       VARCHAR(8) NOT NULL,
  nb_appartements INTEGER
);

CREATE TABLE IMMEUBLE (
  PRIMARY KEY (code_rue, num_immeuble),
  code_rue     VARCHAR(8) NOT NULL,
  num_immeuble VARCHAR(8) NOT NULL,
  nb_etages    INTEGER
);

CREATE TABLE RUE (
  PRIMARY KEY (code_rue),
  code_rue VARCHAR(8) NOT NULL,
  nom_rue  VARCHAR(255)
);

ALTER TABLE APPARTEMENT ADD FOREIGN KEY (code_rue, num_immeuble, num_etage) REFERENCES ETAGE (code_rue, num_immeuble, num_etage);

ALTER TABLE ETAGE ADD FOREIGN KEY (code_rue, num_immeuble) REFERENCES IMMEUBLE (code_rue, num_immeuble);

ALTER TABLE IMMEUBLE ADD FOREIGN KEY (code_rue) REFERENCES RUE (code_rue);
