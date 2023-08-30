- **Affecter** (<ins>projet</ins>, <ins>employé</ins> <sup>u1</sup>, site <sup>u1</sup>)
  - Le champ _projet_ fait partie de la clé primaire de la table. Sa table d'origine (_Projet_) ayant été supprimée, il n'est pas considéré comme clé étrangère.
  - Le champ _employé_ fait partie de la clé primaire de la table. Sa table d'origine (_Employé_) ayant été supprimée, il n'est pas considéré comme clé étrangère. Il fait par contre partie d'une clé alternative matérialisée par la contrainte d'unicité 1.
  - Le champ _site_ est un simple attribut. Sa table d'origine (_Site_) ayant été supprimée, il n'est pas considéré comme clé étrangère. Il fait par contre partie d'une clé alternative matérialisée par la contrainte d'unicité 1.

----


**NB.** Les tables _Employé_, _Projet_ et _Site_ ont été supprimées car elles étaient réduites à la clé primaire de leur entité d'origine.
