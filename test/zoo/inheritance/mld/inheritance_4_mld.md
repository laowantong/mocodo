- **LACUS** (<ins>#magna</ins>, tempor, fugit)
  - Le champ _magna_ constitue la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité-mère _TRISTIS_.
  - Les champs _tempor_ et _fugit_ étaient déjà de simples attributs de l'entité _LACUS_.

- **NEC** (<ins>#magna</ins>, pulvinar, audis, _#magna via mollis_, _#magna via vitae_)
  - Le champ _magna_ constitue la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité-mère _TRISTIS_.
  - Les champs _pulvinar_ et _audis_ étaient déjà de simples attributs de l'entité _NEC_.
  - Le champ _magna via mollis_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _MOLLIS_ à partir de l'entité _LACUS_ en perdant son caractère identifiant.
  - Le champ _magna via vitae_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _VITAE_ à partir de l'entité _SODALES_ en perdant son caractère identifiant.

- **SODALES** (<ins>#magna</ins>, convallis, ipsum)
  - Le champ _magna_ constitue la clé primaire de la table. C'est une clé étrangère qui a migré à partir de l'entité-mère _TRISTIS_.
  - Les champs _convallis_ et _ipsum_ étaient déjà de simples attributs de l'entité _SODALES_.

- **TRISTIS** (<ins>magna</ins>, vestibulum, type)
  - Le champ _magna_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _TRISTIS_.
  - Le champ _vestibulum_ était déjà un simple attribut de l'entité _TRISTIS_.
  - Un champ entier _type_ est ajouté pour indiquer la nature de la spécialisation : 1 pour la première entité-fille, 2 pour la deuxième, etc. Jamais vide, du fait de la contrainte de totalité.

- **ULTRICES** (<ins>_#magna sodales_</ins>, <ins>_#magna lacus_</ins>)
  - Le champ _magna sodales_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _SODALES_.
  - Le champ _magna lacus_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _LACUS_.