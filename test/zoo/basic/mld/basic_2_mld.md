- **CLIENT** (<u>Réf. client</u>, Nom, Prénom, Adresse)
  - Le champ _Réf. client_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _CLIENT_.
  - Les champs _Nom_, _Prénom_ et _Adresse_ étaient déjà de simples attributs de l'entité _CLIENT_.

- **COMMANDE** (<u>Num. commande</u>, Date, Montant, _#Réf. client!_)
  - Le champ _Num. commande_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _COMMANDE_.
  - Les champs _Date_ et _Montant_ étaient déjà de simples attributs de l'entité _COMMANDE_.
  - Le champ à saisie obligatoire _Réf. client_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _PASSER_ à partir de l'entité _CLIENT_ en perdant son caractère identifiant.

- **INCLURE** (<u>_#Num. commande_</u>, <u>_#Réf. produit_</u>, Quantité)
  - Le champ _Num. commande_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _COMMANDE_.
  - Le champ _Réf. produit_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _PRODUIT_.
  - Le champ _Quantité_ était déjà un simple attribut de l'association _INCLURE_.

- **PRODUIT** (<u>Réf. produit</u>, Libellé, Prix unitaire)
  - Le champ _Réf. produit_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _PRODUIT_.
  - Les champs _Libellé_ et _Prix unitaire_ étaient déjà de simples attributs de l'entité _PRODUIT_.
