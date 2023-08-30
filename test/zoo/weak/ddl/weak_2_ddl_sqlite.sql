.open weak;

CREATE TABLE APPARTEMENT (
  code_rue VARCHAR(8),
  num_immeuble VARCHAR(8),
  num_etage VARCHAR(8),
  num_appart VARCHAR(8),
  nb_pieces INTEGER,
  PRIMARY KEY (code_rue, num_immeuble, num_etage, num_appart)
  FOREIGN KEY (code_rue, num_immeuble, num_etage) REFERENCES ETAGE (code_rue, num_immeuble, num_etage)
);

CREATE TABLE ETAGE (
  code_rue VARCHAR(8),
  num_immeuble VARCHAR(8),
  num_etage VARCHAR(8),
  nb_appartements INTEGER,
  PRIMARY KEY (code_rue, num_immeuble, num_etage)
  FOREIGN KEY (code_rue, num_immeuble) REFERENCES IMMEUBLE (code_rue, num_immeuble)
);

CREATE TABLE IMMEUBLE (
  code_rue VARCHAR(8),
  num_immeuble VARCHAR(8),
  nb_etages INTEGER,
  PRIMARY KEY (code_rue, num_immeuble)
  FOREIGN KEY (code_rue) REFERENCES RUE (code_rue)
);

CREATE TABLE RUE (
  code_rue VARCHAR(8),
  nom_rue VARCHAR(255),
  PRIMARY KEY (code_rue)
);
