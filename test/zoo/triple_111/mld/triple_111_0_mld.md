- **Utiliser** (<ins>carnet</ins> <sup>u1</sup>, <ins>projet</ins> <sup>u2</sup>, technicien <sup>u1 u2</sup>)
  - Le champ _carnet_ fait partie de la clé primaire de la table. Sa table d'origine (_Carnet_) ayant été supprimée, il n'est pas considéré comme clé étrangère. Il fait par contre partie d'une clé alternative matérialisée par la contrainte d'unicité 1.
  - Le champ _projet_ fait partie de la clé primaire de la table. Sa table d'origine (_Projet_) ayant été supprimée, il n'est pas considéré comme clé étrangère. Il fait par contre partie d'une clé alternative matérialisée par la contrainte d'unicité 2.
  - Le champ _technicien_ est un simple attribut. Sa table d'origine (_Technicien_) ayant été supprimée, il n'est pas considéré comme clé étrangère. Il fait par contre partie de clés alternatives matérialisées par les contraintes d'unicité 1 et 2.

----


**NB.** Les tables _Carnet_, _Projet_ et _Technicien_ ont été supprimées car elles étaient réduites à la clé primaire de leur entité d'origine.
