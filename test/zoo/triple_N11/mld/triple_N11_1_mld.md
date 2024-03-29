- **Affecter** (<ins>_#projet_</ins>, <ins>_#employé_</ins> <sup>u1</sup>, _#site_ <sup>u1</sup>)
  - Le champ _projet_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _Projet_.
  - Le champ _employé_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _Employé_. Il obéit en outre à la contrainte d'unicité 1.
  - Le champ _site_ est une clé étrangère. Il a migré directement à partir de l'entité _Site_ en perdant son caractère identifiant. Il obéit en outre à la contrainte d'unicité 1.

- **Employé** (<ins>employé</ins>, nom employé)
  - Le champ _employé_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Employé_.
  - Le champ _nom employé_ était déjà un simple attribut de l'entité _Employé_.

- **Projet** (<ins>projet</ins>, libellé)
  - Le champ _projet_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Projet_.
  - Le champ _libellé_ était déjà un simple attribut de l'entité _Projet_.

- **Site** (<ins>site</ins>, position)
  - Le champ _site_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Site_.
  - Le champ _position_ était déjà un simple attribut de l'entité _Site_.
