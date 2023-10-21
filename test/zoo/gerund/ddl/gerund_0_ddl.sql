CREATE TABLE LIGNE_DE_COMMANDE (
  PRIMARY KEY (commande, produit),
  commande VARCHAR(42) NOT NULL,
  produit  VARCHAR(42) NOT NULL,
  quantite INTEGER
);
