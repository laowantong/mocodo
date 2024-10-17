- **Commande** (<u>commande</u>, date)
  - Le champ _commande_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Commande_.
  - Le champ _date_ était déjà un simple attribut de l'entité _Commande_.

- **Ligne de commande** (<u>_#commande_</u>, <u>_#produit_</u>, quantité)
  - Le champ _commande_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité _Commande_ pour renforcer l'identifiant.
  - Le champ _produit_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité _Produit_ pour renforcer l'identifiant.
  - Le champ _quantité_ était déjà un simple attribut de l'entité _Ligne de commande_.

- **Produit** (<u>produit</u>, libellé)
  - Le champ _produit_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Produit_.
  - Le champ _libellé_ était déjà un simple attribut de l'entité _Produit_.
