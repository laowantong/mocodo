- **Bataille** (<ins>nom bataille</ins>, lieu, date)
  - Le champ _nom bataille_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Bataille_.
  - Les champs _lieu_ et _date_ étaient déjà de simples attributs de l'entité _Bataille_.

- **Trophée** (<ins>numéro</ins>, type, état, _#nom villageois!_, _#nom bataille!_)
  - Le champ _numéro_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Trophée_.
  - Les champs _type_ et _état_ étaient déjà de simples attributs de l'entité _Trophée_.
  - Le champ à saisie obligatoire _nom villageois_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _Récolter_ à partir de l'entité _Villageois_ en perdant son caractère identifiant.
  - Le champ à saisie obligatoire _nom bataille_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _Récolter_ à partir de l'entité _Bataille_ en perdant son caractère identifiant.

- **Villageois** (<ins>nom villageois</ins>, adresse, fonction)
  - Le champ _nom villageois_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _Villageois_.
  - Les champs _adresse_ et _fonction_ étaient déjà de simples attributs de l'entité _Villageois_.
