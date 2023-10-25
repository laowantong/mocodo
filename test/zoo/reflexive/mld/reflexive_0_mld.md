- **COMPOSER** (<ins>pièce composante</ins>, <ins>pièce composée</ins>)
  - Les champs _pièce composante_ et _pièce composée_ constituent la clé primaire de la table. Leur table d'origine (_PIÈCE_) ayant été supprimée, ils ne sont pas considérés comme clés étrangères.

- **HOMME** (<ins>Num. SS</ins>, Nom, Prénom, _#Num. SS père?_)
  - Le champ _Num. SS_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _HOMME_.
  - Les champs _Nom_ et _Prénom_ étaient déjà de simples attributs de l'entité _HOMME_.
  - Le champ à saisie facultative _Num. SS père_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _ENGENDRER_ à partir de l'entité _HOMME_ en perdant son caractère identifiant.
<br>
----


**NB.** La table _PIÈCE_ a été supprimée car elle était réduite à la clé primaire de son entité d'origine. Pour conserver une telle table, suffixez d'un « + » le nom de l'entité correspondante dans sa définition.
