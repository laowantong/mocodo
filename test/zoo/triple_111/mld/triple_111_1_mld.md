- **Projet** (<u>projet</u>, libellé)
  - Le champ _projet_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Projet_.
  - Le champ _libellé_ était déjà un simple attribut de l'entité _Projet_.

- **Technicien** (<u>technicien</u>, nom technicien)
  - Le champ _technicien_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Technicien_.
  - Le champ _nom technicien_ était déjà un simple attribut de l'entité _Technicien_.

- **Utiliser** (<u>carnet</u> <sup>u1</sup>, <u>_#projet_</u> <sup>u2</sup>, _#technicien_ <sup>u1 u2</sup>)
  - Le champ _carnet_ fait partie de la clé primaire de la table. Sa table d'origine (_Carnet_) ayant été supprimée, il n'est pas considéré comme clé étrangère. Il obéit par contre à la contrainte d'unicité 1.
  - Le champ _projet_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _Projet_. Il obéit en outre à la contrainte d'unicité 2.
  - Le champ _technicien_ est une clé étrangère. Il a migré directement à partir de l'entité _Technicien_ en perdant son caractère identifiant. Il obéit en outre aux contraintes d'unicité 1 et 2.
<br>
----


**NB.** La table _Carnet_ a été supprimée car elle était réduite à la clé primaire de son entité d'origine. Pour conserver de telles tables, préfixez d'un « + » la définition des entités d'origine.
