- **Disponibilité** (<u>_#semaine_</u>, <u>voilier</u>)
  - Le champ _semaine_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité _Semaine_ pour renforcer l'identifiant.
  - Le champ _voilier_ fait partie de la clé primaire de la table. Il a migré à partir de l'entité _Voilier_ pour renforcer l'identifiant. Cependant, comme la table créée à partir de cette entité a été supprimée, il n'est pas considéré comme clé étrangère.

- **Réservation** (<u>id résa</u>, num résa <sup>u1</sup>, arrhes, date réservation, _#semaine_ <sup>u2</sup>, _#voilier_ <sup>u2</sup>)
  - Le champ _id résa_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Réservation_.
  - Le champ _num résa_ était déjà un simple attribut de l'entité _Réservation_. Il obéit à la contrainte d'unicité 1.
  - Les champs _arrhes_ et _date réservation_ étaient déjà de simples attributs de l'entité _Réservation_.
  - Les champs _semaine_ et _voilier_ sont des clés étrangères. Ils ont migré par l'association de dépendance fonctionnelle _DF_ à partir de l'entité _Disponibilité_ en perdant leur caractère identifiant. Ils obéissent en outre à la contrainte d'unicité 2.

- **Semaine** (<u>semaine</u>, date début <sup>u1</sup>)
  - Le champ _semaine_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Semaine_.
  - Le champ _date début_ était déjà un simple attribut de l'entité _Semaine_. Il obéit à la contrainte d'unicité 1.
<br>
----


**NB.** La table _Voilier_ a été supprimée car elle était réduite à la clé primaire de son entité d'origine. Pour conserver de telles tables, préfixez d'un « + » la définition des entités d'origine.
