- **Réservation** (<u>num résa</u>, arrhes, date résa, _#num voilier_ <sup>u1</sup>, _#num semaine_ <sup>u1</sup>, tarif)
  - Le champ _num résa_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Réservation_.
  - Les champs _arrhes_ et _date résa_ étaient déjà de simples attributs de l'entité _Réservation_.
  - Le champ _num voilier_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _Offrir_ à partir de l'entité _Voilier_ en perdant son caractère identifiant. Il obéit en outre à la contrainte d'unicité 1.
  - Le champ _num semaine_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _Offrir_ à partir de l'entité _Semaine_ en perdant son caractère identifiant. Il obéit en outre à la contrainte d'unicité 1.
  - Le champ _tarif_ a migré à partir de l'association de dépendance fonctionnelle _Offrir_.

- **Semaine** (<u>num semaine</u>, date début <sup>u1</sup>)
  - Le champ _num semaine_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Semaine_.
  - Le champ _date début_ était déjà un simple attribut de l'entité _Semaine_. Il obéit à la contrainte d'unicité 1.

- **Voilier** (<u>num voilier</u>, longueur)
  - Le champ _num voilier_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Voilier_.
  - Le champ _longueur_ était déjà un simple attribut de l'entité _Voilier_.
