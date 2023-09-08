- **Disponibilité** (<ins>_#semaine_</ins>, <ins>_#voilier_</ins>)
  - Le champ _semaine_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité _Semaine_ pour renforcer l'identifiant.
  - Le champ _voilier_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité _Voilier_ pour renforcer l'identifiant. La table correspondante ayant été supprimée, il n'est pas considéré comme clé étrangère.

- **Réservation** (<ins>id résa</ins>, num résa <sup>u1</sup>, arrhes, date réservation, _#semaine_ <sup>u2</sup>, _#voilier_ <sup>u2</sup>)
  - Le champ _id résa_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Réservation_.
  - Le champ _num résa_ était déjà un simple attribut de l'entité _Réservation_. Il obéit à la contrainte d'unicité 1.
  - Les champs _arrhes_ et _date réservation_ étaient déjà de simples attributs de l'entité _Réservation_.
  - Le champ _semaine_ est une clé étrangère. Il a migré directement à partir de l'entité _Disponibilité_ en perdant son caractère identifiant. Il obéit en outre à la contrainte d'unicité 2.
  - Le champ _voilier_ est une clé étrangère. Il a migré directement à partir de l'entité _Disponibilité_ en perdant son caractère identifiant. Il obéit en outre à la contrainte d'unicité 2.

- **Semaine** (<ins>semaine</ins>, date début <sup>u1</sup>)
  - Le champ _semaine_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Semaine_.
  - Le champ _date début_ était déjà un simple attribut de l'entité _Semaine_. Il obéit à la contrainte d'unicité 1.

----


**NB.** La table _Voilier_ a été supprimée car elle était réduite à la clé primaire de son entité d'origine.