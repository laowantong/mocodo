CREATE TABLE CONTRAT (
  PRIMARY KEY (num_prof, date_contrat),
  num_prof                VARCHAR(8) NOT NULL,
  date_contrat            DATE NOT NULL,
  salaire_horaire_contrat VARCHAR(42)
);

CREATE TABLE PROFESSEUR (
  PRIMARY KEY (num_prof),
  num_prof              VARCHAR(8) NOT NULL,
  nom_prof              VARCHAR(255),
  prenom_prof           VARCHAR(255),
  telephone_prof        VARCHAR(20),
  statut_vacataire      VARCHAR(20) NULL,
  date_embauche_salarie DATE NULL,
  echelon_salarie       VARCHAR(42) NULL,
  salaire_salarie       VARCHAR(42) NULL
);

ALTER TABLE CONTRAT ADD FOREIGN KEY (num_prof) REFERENCES PROFESSEUR (num_prof);
