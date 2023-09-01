- **Ligne de commande** (<ins>_#commande_</ins>, <ins>_#produit_</ins>, quantité)
  - Le champ _commande_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité _Commande_ pour renforcer l'identifiant. La table correspondante ayant été supprimée, il n'est pas considéré comme clé étrangère.
  - Le champ _produit_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité _Produit_ pour renforcer l'identifiant. La table correspondante ayant été supprimée, il n'est pas considéré comme clé étrangère.
  - Le champ _quantité_ était déjà un simple attribut de l'entité _Ligne de commande_.

----


**NB.** Les tables _Commande_ et _Produit_ ont été supprimées car elles étaient réduites à la clé primaire de leur entité d'origine.
