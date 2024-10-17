- **COMPOSER** (<u>pièce composante</u>, <u>pièce composée</u>)
  - Les champs _pièce composante_ et _pièce composée_ constituent la clé primaire de la table. Leur table d'origine (_PIÈCE_) ayant été supprimée, ils ne sont pas considérés comme clés étrangères.

- **HOMME** (<u>Num. SS</u>, Nom, Prénom, _#Num. SS père?_)
  - Le champ _Num. SS_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _HOMME_.
  - Les champs _Nom_ et _Prénom_ étaient déjà de simples attributs de l'entité _HOMME_.
  - Le champ à saisie facultative _Num. SS père_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _ENGENDRER_ à partir de l'entité _HOMME_ en perdant son caractère identifiant.
<br>
----


**NB.** La table _PIÈCE_ a été supprimée car elle était réduite à la clé primaire de son entité d'origine. Pour conserver de telles tables, préfixez d'un « + » la définition des entités d'origine.
