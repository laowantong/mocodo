CREATE TABLE LIGNE_DE_COMMANDE (
  commande VARCHAR(42) NOT NULL,
  produit VARCHAR(42) NOT NULL,
  quantite INTEGER,
  PRIMARY KEY (commande, produit)
);
