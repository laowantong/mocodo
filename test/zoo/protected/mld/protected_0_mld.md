- **EROS** (<ins>congue</ins>)
  - Le champ _congue_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _EROS_.

- **LACUS** (<ins>blandit</ins>, elit)
  - Le champ _blandit_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _LACUS_.
  - Le champ _elit_ était déjà un simple attribut de l'entité _LACUS_.

- **LIGULA** (<ins>_#blandit_</ins>, _#congue!_, metus)
  - **Avertissement.** Table résultant de la conversion forcée d'une association DF.
  - Le champ _blandit_ constitue la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _LACUS_.
  - Le champ à saisie obligatoire _congue_ est une clé étrangère. Il a migré directement à partir de l'entité _EROS_ en perdant son caractère identifiant.
  - Le champ _metus_ était déjà un simple attribut de l'association _LIGULA_.
