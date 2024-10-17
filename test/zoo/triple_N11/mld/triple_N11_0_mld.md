- **Affecter** (<u>projet</u>, <u>employé</u> <sup>u1</sup>, site <sup>u1</sup>)
  - Le champ _projet_ fait partie de la clé primaire de la table. Sa table d'origine (_Projet_) ayant été supprimée, il n'est pas considéré comme clé étrangère.
  - Le champ _employé_ fait partie de la clé primaire de la table. Sa table d'origine (_Employé_) ayant été supprimée, il n'est pas considéré comme clé étrangère. Il obéit par contre à la contrainte d'unicité 1.
  - Le champ _site_ est un simple attribut. Il a migré directement à partir de l'entité _Site_ en perdant son caractère identifiant. Cependant, comme la table créée à partir de cette entité a été supprimée, il n'est pas considéré comme clé étrangère. Il obéit par contre à la contrainte d'unicité 1.
<br>
----


**NB.** Les tables _Employé_, _Projet_ et _Site_ ont été supprimées car elles étaient réduites à la clé primaire de leur entité d'origine. Pour conserver de telles tables, préfixez d'un « + » la définition des entités d'origine.
