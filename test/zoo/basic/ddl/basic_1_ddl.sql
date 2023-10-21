CREATE TABLE CLIENT (
  PRIMARY KEY (ref_client),
  ref_client VARCHAR(8) NOT NULL,
  nom        VARCHAR(255),
  prenom     VARCHAR(255),
  adresse    VARCHAR(30)
);

CREATE TABLE COMMANDE (
  PRIMARY KEY (num_commande),
  num_commande VARCHAR(8) NOT NULL,
  date         DATE,
  montant      DECIMAL(10,2),
  ref_client   VARCHAR(8) NOT NULL
);

CREATE TABLE INCLURE (
  PRIMARY KEY (num_commande, ref_produit),
  num_commande VARCHAR(8) NOT NULL,
  ref_produit  VARCHAR(8) NOT NULL,
  quantite     INTEGER
);

CREATE TABLE PRODUIT (
  PRIMARY KEY (ref_produit),
  ref_produit   VARCHAR(8) NOT NULL,
  libelle       VARCHAR(50),
  prix_unitaire DECIMAL(10,2)
);

ALTER TABLE COMMANDE ADD FOREIGN KEY (ref_client) REFERENCES CLIENT (ref_client);

ALTER TABLE INCLURE ADD FOREIGN KEY (ref_produit) REFERENCES PRODUIT (ref_produit);
ALTER TABLE INCLURE ADD FOREIGN KEY (num_commande) REFERENCES COMMANDE (num_commande);
