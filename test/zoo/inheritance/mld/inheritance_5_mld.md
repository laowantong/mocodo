- **LACUS** (<u>magna</u>, vestibulum, tempor, fugit)
  - Le champ _magna_ constitue la clé primaire de la table. Il était clé primaire de l'entité-mère _TRISTIS_ (supprimée).
  - Le champ _vestibulum_ est un simple attribut. Il était simple attribut de l'entité-mère _TRISTIS_ (supprimée).
  - Les champs _tempor_ et _fugit_ étaient déjà de simples attributs de l'entité _LACUS_.

- **NEC** (<u>magna</u>, vestibulum, pulvinar, audis, _#magna via_mollis!_, _#magna via_vitae!_)
  - Le champ _magna_ constitue la clé primaire de la table. Il était clé primaire de l'entité-mère _TRISTIS_ (supprimée).
  - Le champ _vestibulum_ est un simple attribut. Il était simple attribut de l'entité-mère _TRISTIS_ (supprimée).
  - Les champs _pulvinar_ et _audis_ étaient déjà de simples attributs de l'entité _NEC_.
  - Le champ à saisie obligatoire _magna via_mollis_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _MOLLIS_ à partir de l'entité _LACUS_ en perdant son caractère identifiant.
  - Le champ à saisie obligatoire _magna via_vitae_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _VITAE_ à partir de l'entité _SODALES_ en perdant son caractère identifiant.

- **SODALES** (<u>magna</u>, vestibulum, convallis, ipsum)
  - Le champ _magna_ constitue la clé primaire de la table. Il était clé primaire de l'entité-mère _TRISTIS_ (supprimée).
  - Le champ _vestibulum_ est un simple attribut. Il était simple attribut de l'entité-mère _TRISTIS_ (supprimée).
  - Les champs _convallis_ et _ipsum_ étaient déjà de simples attributs de l'entité _SODALES_.

- **ULTRICES** (<u>_#magna sodales_</u>, <u>_#magna lacus_</u>)
  - Le champ _magna sodales_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _SODALES_.
  - Le champ _magna lacus_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _LACUS_.
