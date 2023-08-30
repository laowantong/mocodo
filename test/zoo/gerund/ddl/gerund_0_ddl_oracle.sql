CREATE TABLE LIGNE_DE_COMMANDE (
  commande VARCHAR(42),
  produit VARCHAR(42),
  quantite INTEGER,
  PRIMARY KEY (commande, produit)
);
