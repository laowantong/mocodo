- **Gérer** (<u>_#ingénieur_</u>, <u>_#projet_</u>, _#responsable!_)
  - Le champ _ingénieur_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _Ingénieur_.
  - Le champ _projet_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _Projet_.
  - Le champ à saisie obligatoire _responsable_ est une clé étrangère. Il a migré directement à partir de l'entité _Responsable_ en perdant son caractère identifiant.

- **Ingénieur** (<u>ingénieur</u>, nom ingénieur)
  - Le champ _ingénieur_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Ingénieur_.
  - Le champ _nom ingénieur_ était déjà un simple attribut de l'entité _Ingénieur_.

- **Projet** (<u>projet</u>, libellé projet)
  - Le champ _projet_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Projet_.
  - Le champ _libellé projet_ était déjà un simple attribut de l'entité _Projet_.

- **Responsable** (<u>responsable</u>, nom responsable)
  - Le champ _responsable_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Responsable_.
  - Le champ _nom responsable_ était déjà un simple attribut de l'entité _Responsable_.
