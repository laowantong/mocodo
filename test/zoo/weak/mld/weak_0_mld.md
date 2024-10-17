- **Exemplaire** (<u>œuvre</u>, <u>exemplaire</u>, foobar)
  - Le champ _œuvre_ fait partie de la clé primaire de la table. Il a migré à partir de l'entité _Œuvre_ pour renforcer l'identifiant. Cependant, comme la table créée à partir de cette entité a été supprimée, il n'est pas considéré comme clé étrangère.
  - Le champ _exemplaire_ fait partie de la clé primaire de la table. C'était déjà un identifiant de l'entité _Exemplaire_.
  - Le champ _foobar_ a migré à partir de l'association de dépendance fonctionnelle _DF_.
<br>
----


**NB.** La table _Œuvre_ a été supprimée car elle était réduite à la clé primaire de son entité d'origine. Pour conserver de telles tables, préfixez d'un « + » la définition des entités d'origine.
