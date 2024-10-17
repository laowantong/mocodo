- **LACUS** (<u>_#magna_</u>, tempor, fugit)
  - Le champ _magna_ constitue la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité-mère _TRISTIS_.
  - Les champs _tempor_ et _fugit_ étaient déjà de simples attributs de l'entité _LACUS_.

- **NEC** (<u>_#magna_</u>, pulvinar, audis, _#magna via_mollis!_, _#magna via_vitae!_)
  - Le champ _magna_ constitue la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité-mère _TRISTIS_.
  - Les champs _pulvinar_ et _audis_ étaient déjà de simples attributs de l'entité _NEC_.
  - Le champ à saisie obligatoire _magna via_mollis_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _MOLLIS_ à partir de l'entité _LACUS_ en perdant son caractère identifiant.
  - Le champ à saisie obligatoire _magna via_vitae_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _VITAE_ à partir de l'entité _SODALES_ en perdant son caractère identifiant.

- **SODALES** (<u>_#magna_</u>, convallis, ipsum)
  - Le champ _magna_ constitue la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité-mère _TRISTIS_.
  - Les champs _convallis_ et _ipsum_ étaient déjà de simples attributs de l'entité _SODALES_.

- **TRISTIS** (<u>magna</u>, vestibulum, type!)
  - Le champ _magna_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _TRISTIS_.
  - Le champ _vestibulum_ était déjà un simple attribut de l'entité _TRISTIS_.
  - Un discriminateur à saisie obligatoire _type_ est ajouté pour indiquer la nature de la spécialisation. Jamais vide, du fait de la contrainte de totalité.

- **ULTRICES** (<u>_#magna sodales_</u>, <u>_#magna lacus_</u>)
  - Le champ _magna sodales_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _SODALES_.
  - Le champ _magna lacus_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _LACUS_.
