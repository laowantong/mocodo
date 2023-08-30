- **CLIENT** (<ins>Réf. client</ins>, Nom, Prénom, Adresse)
  - Le champ _Réf. client_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _CLIENT_.
  - Les champs _Nom_, _Prénom_ et _Adresse_ étaient déjà de simples attributs de l'entité _CLIENT_.

- **COMMANDE** (<ins>Num commande</ins>, Date, Montant)
  - Le champ _Num commande_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _COMMANDE_.
  - Les champs _Date_ et _Montant_ étaient déjà de simples attributs de l'entité _COMMANDE_.

- **INCLURE** (<ins>_#Num commande_</ins>, <ins>_#Réf. produit_</ins>, Quantité)
  - Le champ _Num commande_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _COMMANDE_.
  - Le champ _Réf. produit_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _PRODUIT_.
  - Le champ _Quantité_ était déjà un simple attribut de l'association _INCLURE_.

- **PASSER** (<ins>_#Réf. client_</ins>, <ins>_#Num commande_</ins>)
  - Le champ _Réf. client_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _CLIENT_.
  - Le champ _Num commande_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _COMMANDE_.

- **PRODUIT** (<ins>Réf. produit</ins>, Libellé, Prix unitaire)
  - Le champ _Réf. produit_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _PRODUIT_.
  - Les champs _Libellé_ et _Prix unitaire_ étaient déjà de simples attributs de l'entité _PRODUIT_.
