- **Agence** (<u>id. agence</u>, nom agence)
  - Le champ _id. agence_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Agence_.
  - Le champ _nom agence_ était déjà un simple attribut de l'entité _Agence_.

- **Direction régionale** (<u>id. dir.</u>, nom dir.)
  - Le champ _id. dir._ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Direction régionale_.
  - Le champ _nom dir._ était déjà un simple attribut de l'entité _Direction régionale_.

- **Superviser** (<u>_#id. agence_</u>, _#id. dir.!_)
  - **Avertissement.** Table résultant de la conversion forcée d'une association DF.
  - Le champ _id. agence_ constitue la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _Agence_.
  - Le champ à saisie obligatoire _id. dir._ est une clé étrangère. Il a migré directement à partir de l'entité _Direction régionale_ en perdant son caractère identifiant.
