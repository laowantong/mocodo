- **Exemplaire** (<u>_#œuvre_</u>, <u>exemplaire</u>, nb pages, date achat, foobar)
  - Le champ _œuvre_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité _Œuvre_ pour renforcer l'identifiant.
  - Le champ _exemplaire_ fait partie de la clé primaire de la table. C'était déjà un identifiant de l'entité _Exemplaire_.
  - Les champs _nb pages_ et _date achat_ étaient déjà de simples attributs de l'entité _Exemplaire_.
  - Le champ _foobar_ a migré à partir de l'association de dépendance fonctionnelle _DF_.

- **Œuvre** (<u>œuvre</u>, auteur)
  - Le champ _œuvre_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Œuvre_.
  - Le champ _auteur_ était déjà un simple attribut de l'entité _Œuvre_.
