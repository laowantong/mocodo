- **Projet** (<ins>projet</ins>, libellé)
  - Le champ _projet_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Projet_.
  - Le champ _libellé_ était déjà un simple attribut de l'entité _Projet_.

- **Technicien** (<ins>technicien</ins>, nom technicien)
  - Le champ _technicien_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Technicien_.
  - Le champ _nom technicien_ était déjà un simple attribut de l'entité _Technicien_.

- **Utiliser** (<ins>carnet</ins> <sup>u1</sup>, <ins>_#projet_</ins> <sup>u2</sup>, _#technicien_ <sup>u1 u2</sup>)
  - Le champ _carnet_ fait partie de la clé primaire de la table. Sa table d'origine (_Carnet_) ayant été supprimée, il n'est pas considéré comme clé étrangère. Il fait par contre partie d'une clé alternative matérialisée par la contrainte d'unicité 1.
  - Le champ _projet_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _Projet_. Il fait en outre partie d'une clé alternative matérialisée par la contrainte d'unicité 2.
  - Le champ _technicien_ est une clé étrangère. Il a migré directement à partir de l'entité _Technicien_ en perdant son caractère identifiant. Il fait en outre partie de clés alternatives matérialisées par les contraintes d'unicité 1 et 2.

----


**NB.** La table _Carnet_ a été supprimée car elle était réduite à la clé primaire de son entité d'origine.
