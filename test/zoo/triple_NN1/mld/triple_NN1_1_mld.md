- **Gérer** (<ins>_#ingénieur_</ins>, <ins>_#projet_</ins>, _#responsable!_)
  - Le champ _ingénieur_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _Ingénieur_.
  - Le champ _projet_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _Projet_.
  - Le champ à saisie obligatoire _responsable_ est une clé étrangère. Il a migré directement à partir de l'entité _Responsable_ en perdant son caractère identifiant.

- **Ingénieur** (<ins>ingénieur</ins>, nom ingénieur)
  - Le champ _ingénieur_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Ingénieur_.
  - Le champ _nom ingénieur_ était déjà un simple attribut de l'entité _Ingénieur_.

- **Projet** (<ins>projet</ins>, libellé projet)
  - Le champ _projet_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Projet_.
  - Le champ _libellé projet_ était déjà un simple attribut de l'entité _Projet_.

- **Responsable** (<ins>responsable</ins>, nom responsable)
  - Le champ _responsable_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Responsable_.
  - Le champ _nom responsable_ était déjà un simple attribut de l'entité _Responsable_.
