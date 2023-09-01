- **Gérer** (<ins>ingénieur</ins>, <ins>projet</ins>, responsable)
  - Le champ _ingénieur_ fait partie de la clé primaire de la table. Sa table d'origine (_Ingénieur_) ayant été supprimée, il n'est pas considéré comme clé étrangère.
  - Le champ _projet_ fait partie de la clé primaire de la table. Sa table d'origine (_Projet_) ayant été supprimée, il n'est pas considéré comme clé étrangère.
  - Le champ _responsable_ est un simple attribut. Il a migré par l'association de dépendance fonctionnelle _Gérer_ à partir de l'entité _Responsable_ en perdant son caractère identifiant. Cependant, comme la table créée à partir de cette entité a été supprimée, il n'est pas considéré comme clé étrangère.

----


**NB.** Les tables _Ingénieur_, _Projet_ et _Responsable_ ont été supprimées car elles étaient réduites à la clé primaire de leur entité d'origine.
