- **ALIQUET** (<u>_#magna_</u>, <u>_#tellus_</u>)
  - Le champ _magna_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _TRISTIS_.
  - Le champ _tellus_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _DIGNISSIM_.

- **CONSEQUAT** (<u>fermentum</u>, dederit)
  - Le champ _fermentum_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _CONSEQUAT_.
  - Le champ _dederit_ était déjà un simple attribut de l'entité _CONSEQUAT_.

- **CURABITUR** (<u>gravida</u>, amor)
  - Le champ _gravida_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _CURABITUR_.
  - Le champ _amor_ était déjà un simple attribut de l'entité _CURABITUR_.

- **DIGNISSIM** (<u>tellus</u>, terra)
  - Le champ _tellus_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _DIGNISSIM_.
  - Le champ _terra_ était déjà un simple attribut de l'entité _DIGNISSIM_.

- **LIBERO** (<u>posuere</u>, lacrima)
  - Le champ _posuere_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _LIBERO_.
  - Le champ _lacrima_ était déjà un simple attribut de l'entité _LIBERO_.

- **QUAM** (<u>cras</u>, sed, _#magna!_)
  - Le champ _cras_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _QUAM_.
  - Le champ _sed_ était déjà un simple attribut de l'entité _QUAM_.
  - Le champ à saisie obligatoire _magna_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _VITAE_ à partir de l'entité _TRISTIS_ en perdant son caractère identifiant.

- **SUSCIPIT** (<u>orci</u>, lorem, _#magna!_)
  - Le champ _orci_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _SUSCIPIT_.
  - Le champ _lorem_ était déjà un simple attribut de l'entité _SUSCIPIT_.
  - Le champ à saisie obligatoire _magna_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _RHONCUS_ à partir de l'entité _TRISTIS_ en perdant son caractère identifiant.

- **TRISTIS** (<u>magna</u>, vestibulum, _#fermentum!_, type!, convallis?, ipsum?, pulvinar?, audis?, _#gravida?_, tempor?, fugit?)
  - Le champ _magna_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _TRISTIS_.
  - Le champ _vestibulum_ était déjà un simple attribut de l'entité _TRISTIS_.
  - Le champ à saisie obligatoire _fermentum_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _ELIT_ à partir de l'entité _CONSEQUAT_ en perdant son caractère identifiant.
  - Un discriminateur à saisie obligatoire _type_ est ajouté pour indiquer la nature de la spécialisation. Jamais vide, du fait de la contrainte de totalité.
  - Le champ à saisie facultative _convallis_ a migré à partir de l'entité-fille _SODALES_ (supprimée).
  - Le champ à saisie facultative _ipsum_ a migré à partir de l'entité-fille _SODALES_ (supprimée).
  - Le champ à saisie facultative _pulvinar_ a migré à partir de l'entité-fille _NEC_ (supprimée).
  - Le champ à saisie facultative _audis_ a migré à partir de l'entité-fille _NEC_ (supprimée).
  - Le champ à saisie facultative _gravida_ est une clé étrangère. Il a migré à partir de l'entité-fille _NEC_ (supprimée) dans laquelle il avait déjà migré à partir de l'entité _CURABITUR_.
  - Le champ à saisie facultative _tempor_ a migré à partir de l'entité-fille _LACUS_ (supprimée).
  - Le champ à saisie facultative _fugit_ a migré à partir de l'entité-fille _LACUS_ (supprimée).

- **ULTRICES** (<u>_#posuere_</u>, <u>_#magna_</u>)
  - Le champ _posuere_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _LIBERO_.
  - Le champ _magna_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _TRISTIS_.
