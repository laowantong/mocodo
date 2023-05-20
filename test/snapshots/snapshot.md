# Snapshots
## Source

```
:
    PEUT COHABITER AVEC, 0N ESPÈCE, 0N [commensale] ESPÈCE: nb. max. commensaux
:
:
:

PEUT VIVRE DANS, 1N ESPÈCE, 1N ENCLOS: nb. max. congénères
ESPÈCE: code espèce, libellé
  DF, 0N ESPÈCE, _11 ANIMAL
:
  CARNIVORE: quantité viande

ENCLOS: num. enclos
      OCCUPE, 1N ANIMAL, /1N PÉRIODE, 1N ENCLOS
  ANIMAL: nom, sexe, date naissance, date décès
  /\ ANIMAL <= CARNIVORE, HERBIVORE: type alimentation
:

:
      PÉRIODE: date début, _date fin
    A MÈRE, 01 ANIMAL, 0N> [mère] ANIMAL
:
  HERBIVORE: plante préférée
```

## SVG output

### Static

![](snapshot_static.svg)

### Dynamic

![](snapshot.svg)

## Relational output

### `debug.json`

```markdown
| Relation | Attribute | `nature` | `adjacent_source` | `outer_source` |
|---|---|---|---|---|
| ANIMAL | code espèce | `strengthening_primary_key` | ESPÈCE | ESPÈCE |
| ANIMAL | nom | `primary_key` | None | None |
| ANIMAL | sexe | `normal_attribute` | None | None |
| ANIMAL | date naissance | `normal_attribute` | None | None |
| ANIMAL | date décès | `normal_attribute` | None | None |
| ANIMAL | code espèce mère | `foreign_key` | ANIMAL | ANIMAL |
| ANIMAL | nom mère | `foreign_key` | ANIMAL | ANIMAL |
| ANIMAL | type alimentation | `deleted_child_discriminant_` | None | None |
| ANIMAL | CARNIVORE | `deleted_child_entity_name` | CARNIVORE | CARNIVORE |
| ANIMAL | quantité viande | `deleted_child_attribute` | CARNIVORE | None |
| ANIMAL | HERBIVORE | `deleted_child_entity_name` | HERBIVORE | HERBIVORE |
| ANIMAL | plante préférée | `deleted_child_attribute` | HERBIVORE | None |
| ESPÈCE | code espèce | `primary_key` | None | None |
| ESPÈCE | libellé | `normal_attribute` | None | None |
| OCCUPE | code espèce | `primary_foreign_key` | ANIMAL | ANIMAL |
| OCCUPE | nom | `primary_foreign_key` | ANIMAL | ANIMAL |
| OCCUPE | num. enclos | `primary_key` | ENCLOS | ENCLOS |
| OCCUPE | date début | `normal_attribute` | PÉRIODE | PÉRIODE |
| OCCUPE | date fin | `normal_attribute` | PÉRIODE | PÉRIODE |
| PEUT COHABITER AVEC | code espèce | `primary_foreign_key` | ESPÈCE | ESPÈCE |
| PEUT COHABITER AVEC | code espèce commensale | `primary_foreign_key` | ESPÈCE | ESPÈCE |
| PEUT COHABITER AVEC | nb. max. commensaux | `association_attribute` | None | None |
| PEUT VIVRE DANS | code espèce | `primary_foreign_key` | ESPÈCE | ESPÈCE |
| PEUT VIVRE DANS | num. enclos | `primary_key` | ENCLOS | ENCLOS |
| PEUT VIVRE DANS | nb. max. congénères | `association_attribute` | None | None |
```

### `dependencies.json`

```graphviz
digraph {
  node [shape=box]
  "ESPÈCE" -> "ANIMAL"
  "ANIMAL" -> "OCCUPE"
  "ESPÈCE" -> "PEUT COHABITER AVEC"
  "ESPÈCE" -> "PEUT VIVRE DANS"
}
```

### `diagram.json`

```plain
%%mocodo
:::
PEUT COHABITER AVEC: #code espèce->ESPÈCE->code espèce, _#code espèce commensale->ESPÈCE->code espèce, nb. max. commensaux
:::


:
PEUT VIVRE DANS: #code espèce->ESPÈCE->code espèce, _num. enclos, nb. max. congénères
:
ESPÈCE: code espèce, libellé
:::


:::
OCCUPE: #code espèce->ANIMAL->code espèce, _#nom->ANIMAL->nom, _num. enclos, date début, date fin
:
ANIMAL: #code espèce->ESPÈCE->code espèce, _nom, sexe, date naissance, date décès, #code espèce mère->ANIMAL->code espèce, #nom mère->ANIMAL->nom, type alimentation, CARNIVORE, quantité viande, HERBIVORE, plante préférée
:
```

### `html.json`

```html
<html>
<head>
<meta charset='utf-8'>
<style>
  #mld .relation { font-variant: small-caps; font-weight: bold }
  #mld .primary { text-decoration: underline }
  #mld .foreign { font-style: oblique }
  #mld .normal { }
</style>
</head>
<body>
<div id='mld'>
<div>
  <span class='relation'>ANIMAL</span> (
    <span class='foreign primary'>#code espèce</span>,
    <span class='primary'>nom</span>,
    <span class='normal'>sexe</span>,
    <span class='normal'>date naissance</span>,
    <span class='normal'>date décès</span>,
    <span class='foreign'>#code espèce mère</span>,
    <span class='foreign'>#nom mère</span>,
    <span class='normal'>type alimentation</span>,
    <span class='normal'>CARNIVORE</span>,
    <span class='normal'>quantité viande</span>,
    <span class='normal'>HERBIVORE</span>,
    <span class='normal'>plante préférée</span>
  )
</div>
<div>
  <span class='relation'>ESPÈCE</span> (
    <span class='primary'>code espèce</span>,
    <span class='normal'>libellé</span>
  )
</div>
<div>
  <span class='relation'>OCCUPE</span> (
    <span class='foreign primary'>#code espèce</span>,
    <span class='foreign primary'>#nom</span>,
    <span class='primary'>num. enclos</span>,
    <span class='normal'>date début</span>,
    <span class='normal'>date fin</span>
  )
</div>
<div>
  <span class='relation'>PEUT COHABITER AVEC</span> (
    <span class='foreign primary'>#code espèce</span>,
    <span class='foreign primary'>#code espèce commensale</span>,
    <span class='normal'>nb. max. commensaux</span>
  )
</div>
<div>
  <span class='relation'>PEUT VIVRE DANS</span> (
    <span class='foreign primary'>#code espèce</span>,
    <span class='primary'>num. enclos</span>,
    <span class='normal'>nb. max. congénères</span>
  )
</div>
</div>
</body>
</html>
```

### `html_verbose.json`

```html
<html>
<head>
<meta charset='utf-8'>
<style>
  #mld .relation { font-variant: small-caps; font-weight: bold }
  #mld .primary { text-decoration: underline }
  #mld .foreign { font-style: oblique }
  #mld .normal { }
  #mld strong { font-weight: bold }
  #mld i { font-style: italic }
  #mld ul { list-style-type:square; margin: 0 0 1em 2em }
</style>
</head>
<body>
<div id='mld'>
<div>
  <details><summary><span class='relation'>ANIMAL</span> (
    <span title='strengthening_primary_key (ESPÈCE)' class='foreign primary'>#code espèce</span>,
    <span title='primary_key (None)' class='primary'>nom</span>,
    <span title='normal_attribute (None)' class='normal'>sexe</span>,
    <span title='normal_attribute (None)' class='normal'>date naissance</span>,
    <span title='normal_attribute (None)' class='normal'>date décès</span>,
    <span title='foreign_key (ANIMAL)' class='foreign'>#code espèce mère</span>,
    <span title='foreign_key (ANIMAL)' class='foreign'>#nom mère</span>,
    <span title='deleted_child_discriminant_ (None)' class='normal'>type alimentation</span>,
    <span title='deleted_child_entity_name (CARNIVORE)' class='normal'>CARNIVORE</span>,
    <span title='deleted_child_attribute (None)' class='normal'>quantité viande</span>,
    <span title='deleted_child_entity_name (HERBIVORE)' class='normal'>HERBIVORE</span>,
    <span title='deleted_child_attribute (None)' class='normal'>plante préférée</span>
  )</summary>
  <ul>
    <li>Le champ <i>code espèce</i> fait partie de la clé primaire de la table. Il a migré à partir de l'entité <i>ESPÈCE</i> pour renforcer l'identifiant.</li>
    <li>Le champ <i>nom</i> fait partie de la clé primaire de la table. C'était déjà un identifiant de l'entité <i>ANIMAL</i>.</li>
    <li>Les champs <i>sexe</i>, <i>date naissance</i> et <i>date décès</i> étaient déjà de simples attributs de l'entité <i>ANIMAL</i>.</li>
    <li>Le champ <i>code espèce mère</i> est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle <i>A MÈRE</i> à partir de l'entité <i>ANIMAL</i> en perdant son caractère identifiant.</li>
    <li>Le champ <i>nom mère</i> est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle <i>A MÈRE</i> à partir de l'entité <i>ANIMAL</i> en perdant son caractère identifiant.</li>
    <li>Un champ entier <i>type alimentation</i> est ajouté pour indiquer la nature de la spécialisation. Il est interprété comme un code binaire : bit 1 pour la première entité-fille, bit 2 pour la deuxième, etc. Peut être vide, du fait de l'absence de contrainte de totalité.</li>
    <li>Un champ booléen <i>CARNIVORE</i> est ajouté pour indiquer si on a affaire ou pas à la spécialisation de même nom.</li>
    <li>Le champ <i>quantité viande</i> a migré à partir de l'entité-fille <i>CARNIVORE</i> (supprimée).</li>
    <li>Un champ booléen <i>HERBIVORE</i> est ajouté pour indiquer si on a affaire ou pas à la spécialisation de même nom.</li>
    <li>Le champ <i>plante préférée</i> a migré à partir de l'entité-fille <i>HERBIVORE</i> (supprimée).</li>
  </ul></details>
</div>

<div>
  <details><summary><span class='relation'>ESPÈCE</span> (
    <span title='primary_key (None)' class='primary'>code espèce</span>,
    <span title='normal_attribute (None)' class='normal'>libellé</span>
  )</summary>
  <ul>
    <li>Le champ <i>code espèce</i> constitue la clé primaire de la table. C'était déjà un identifiant de l'entité <i>ESPÈCE</i>.</li>
    <li>Le champ <i>libellé</i> était déjà un simple attribut de l'entité <i>ESPÈCE</i>.</li>
  </ul></details>
</div>

<div>
  <details><summary><span class='relation'>OCCUPE</span> (
    <span title='primary_foreign_key (ANIMAL)' class='foreign primary'>#code espèce</span>,
    <span title='primary_foreign_key (ANIMAL)' class='foreign primary'>#nom</span>,
    <span title='primary_naturalized_foreign_key (ENCLOS)' class='primary'>num. enclos</span>,
    <span title='demoted_naturalized_foreign_key (PÉRIODE)' class='normal'>date début</span>,
    <span title='demoted_naturalized_foreign_key (PÉRIODE)' class='normal'>date fin</span>
  )</summary>
  <ul>
    <li>Les champs <i>code espèce</i> et <i>nom</i> font partie de la clé primaire de la table. Ce sont des clés étrangères qui ont migré directement à partir de l'entité <i>ANIMAL</i>.</li>
    <li>Le champ <i>num. enclos</i> fait partie de la clé primaire de la table. Sa table d'origine (<i>ENCLOS</i>) ayant été supprimée, il n'est pas considéré comme clé étrangère.</li>
    <li>Le champ <i>date début</i> est un simple attribut. Sa table d'origine, <i>PÉRIODE</i>, ayant été supprimée, il n'est pas considéré comme clé étrangère. Il devrait normalement faire partie de l'identifiant de <i>OCCUPE</i>, mais a été rétrogradé explicitement au rang de simple attribut.</li>
    <li>Le champ <i>date fin</i> est un simple attribut. Sa table d'origine, <i>PÉRIODE</i>, ayant été supprimée, il n'est pas considéré comme clé étrangère. Il devrait normalement faire partie de l'identifiant de <i>OCCUPE</i>, mais a été rétrogradé explicitement au rang de simple attribut.</li>
  </ul></details>
</div>

<div>
  <details><summary><span class='relation'>PEUT COHABITER AVEC</span> (
    <span title='primary_foreign_key (ESPÈCE)' class='foreign primary'>#code espèce</span>,
    <span title='primary_foreign_key (ESPÈCE)' class='foreign primary'>#code espèce commensale</span>,
    <span title='association_attribute (None)' class='normal'>nb. max. commensaux</span>
  )</summary>
  <ul>
    <li>Les champs <i>code espèce</i> et <i>code espèce commensale</i> constituent la clé primaire de la table. Ce sont des clés étrangères qui ont migré directement à partir de l'entité <i>ESPÈCE</i>.</li>
    <li>Le champ <i>nb. max. commensaux</i> était déjà un simple attribut de l'association <i>PEUT COHABITER AVEC</i>.</li>
  </ul></details>
</div>

<div>
  <details><summary><span class='relation'>PEUT VIVRE DANS</span> (
    <span title='primary_foreign_key (ESPÈCE)' class='foreign primary'>#code espèce</span>,
    <span title='primary_naturalized_foreign_key (ENCLOS)' class='primary'>num. enclos</span>,
    <span title='association_attribute (None)' class='normal'>nb. max. congénères</span>
  )</summary>
  <ul>
    <li>Le champ <i>code espèce</i> fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité <i>ESPÈCE</i>.</li>
    <li>Le champ <i>num. enclos</i> fait partie de la clé primaire de la table. Sa table d'origine (<i>ENCLOS</i>) ayant été supprimée, il n'est pas considéré comme clé étrangère.</li>
    <li>Le champ <i>nb. max. congénères</i> était déjà un simple attribut de l'association <i>PEUT VIVRE DANS</i>.</li>
  </ul></details>
</div>
<br><hr><br><div><span><strong>NB.</strong> Les tables <i>ENCLOS</i> et <i>PÉRIODE</i> ont été supprimées car elles étaient réduites à la clé primaire de leur entité d'origine.</span></div>
</div>
</body>
</html>
```

### `json.json`

```json
{
  "title": "Untitled",
  "title_lowercase": "untitled",
  "title_uppercase": "UNTITLED",
  "title_titlecase": "Untitled",
  "deleted_relations": ["ENCLOS", "PÉRIODE"],
  "relations": [
    {
      "this_relation_name": "ANIMAL",
      "this_relation_name_lowercase": "animal",
      "this_relation_name_uppercase": "ANIMAL",
      "this_relation_name_titlecase": "Animal",
      "is_forced": "False",
      "columns": [
        {
          "attribute": "code espèce",
          "raw_label": "code espèce",
          "raw_label_lowercase": "code espèce",
          "raw_label_uppercase": "CODE ESPÈCE",
          "raw_label_titlecase": "Code espèce",
          "disambiguation_number": null,
          "label": "code espèce",
          "label_lowercase": "code espèce",
          "label_uppercase": "CODE ESPÈCE",
          "label_titlecase": "Code espèce",
          "primary": true,
          "nature": "strengthening_primary_key",
          "data_type": null,
          "association_name": "DF",
          "association_name_lower_case": "df",
          "association_name_uppercase": "DF",
          "association_name_titlecase": "Df",
          "leg_note": null,
          "outer_source": "ESPÈCE",
          "outer_source_lowercase": "espèce",
          "outer_source_uppercase": "ESPÈCE",
          "outer_source_titlecase": "Espèce"
        },
        {
          "attribute": "nom",
          "raw_label": "nom",
          "raw_label_lowercase": "nom",
          "raw_label_uppercase": "NOM",
          "raw_label_titlecase": "Nom",
          "disambiguation_number": null,
          "label": "nom",
          "label_lowercase": "nom",
          "label_uppercase": "NOM",
          "label_titlecase": "Nom",
          "primary": true,
          "nature": "primary_key",
          "data_type": null,
          "association_name": null,
          "association_name_lower_case": null,
          "association_name_uppercase": null,
          "association_name_titlecase": null,
          "leg_note": null,
          "outer_source": null,
          "outer_source_lowercase": null,
          "outer_source_uppercase": null,
          "outer_source_titlecase": null
        },
        {
          "attribute": "sexe",
          "raw_label": "sexe",
          "raw_label_lowercase": "sexe",
          "raw_label_uppercase": "SEXE",
          "raw_label_titlecase": "Sexe",
          "disambiguation_number": null,
          "label": "sexe",
          "label_lowercase": "sexe",
          "label_uppercase": "SEXE",
          "label_titlecase": "Sexe",
          "primary": false,
          "nature": "normal_attribute",
          "data_type": null,
          "association_name": null,
          "association_name_lower_case": null,
          "association_name_uppercase": null,
          "association_name_titlecase": null,
          "leg_note": null,
          "outer_source": null,
          "outer_source_lowercase": null,
          "outer_source_uppercase": null,
          "outer_source_titlecase": null
        },
        {
          "attribute": "date naissance",
          "raw_label": "date naissance",
          "raw_label_lowercase": "date naissance",
          "raw_label_uppercase": "DATE NAISSANCE",
          "raw_label_titlecase": "Date naissance",
          "disambiguation_number": null,
          "label": "date naissance",
          "label_lowercase": "date naissance",
          "label_uppercase": "DATE NAISSANCE",
          "label_titlecase": "Date naissance",
          "primary": false,
          "nature": "normal_attribute",
          "data_type": null,
          "association_name": null,
          "association_name_lower_case": null,
          "association_name_uppercase": null,
          "association_name_titlecase": null,
          "leg_note": null,
          "outer_source": null,
          "outer_source_lowercase": null,
          "outer_source_uppercase": null,
          "outer_source_titlecase": null
        },
        {
          "attribute": "date décès",
          "raw_label": "date décès",
          "raw_label_lowercase": "date décès",
          "raw_label_uppercase": "DATE DÉCÈS",
          "raw_label_titlecase": "Date décès",
          "disambiguation_number": null,
          "label": "date décès",
          "label_lowercase": "date décès",
          "label_uppercase": "DATE DÉCÈS",
          "label_titlecase": "Date décès",
          "primary": false,
          "nature": "normal_attribute",
          "data_type": null,
          "association_name": null,
          "association_name_lower_case": null,
          "association_name_uppercase": null,
          "association_name_titlecase": null,
          "leg_note": null,
          "outer_source": null,
          "outer_source_lowercase": null,
          "outer_source_uppercase": null,
          "outer_source_titlecase": null
        },
        {
          "attribute": "code espèce",
          "raw_label": "code espèce",
          "raw_label_lowercase": "code espèce",
          "raw_label_uppercase": "CODE ESPÈCE",
          "raw_label_titlecase": "Code espèce",
          "disambiguation_number": null,
          "label": "code espèce mère",
          "label_lowercase": "code espèce mère",
          "label_uppercase": "CODE ESPÈCE MÈRE",
          "label_titlecase": "Code espèce mère",
          "primary": false,
          "nature": "foreign_key",
          "data_type": null,
          "association_name": "A MÈRE",
          "association_name_lower_case": "a mère",
          "association_name_uppercase": "A MÈRE",
          "association_name_titlecase": "A mère",
          "leg_note": "mère",
          "outer_source": "ANIMAL",
          "outer_source_lowercase": "animal",
          "outer_source_uppercase": "ANIMAL",
          "outer_source_titlecase": "Animal"
        },
        {
          "attribute": "nom",
          "raw_label": "nom",
          "raw_label_lowercase": "nom",
          "raw_label_uppercase": "NOM",
          "raw_label_titlecase": "Nom",
          "disambiguation_number": null,
          "label": "nom mère",
          "label_lowercase": "nom mère",
          "label_uppercase": "NOM MÈRE",
          "label_titlecase": "Nom mère",
          "primary": false,
          "nature": "foreign_key",
          "data_type": null,
          "association_name": "A MÈRE",
          "association_name_lower_case": "a mère",
          "association_name_uppercase": "A MÈRE",
          "association_name_titlecase": "A mère",
          "leg_note": "mère",
          "outer_source": "ANIMAL",
          "outer_source_lowercase": "animal",
          "outer_source_uppercase": "ANIMAL",
          "outer_source_titlecase": "Animal"
        },
        {
          "attribute": "type alimentation",
          "raw_label": "type alimentation",
          "raw_label_lowercase": "type alimentation",
          "raw_label_uppercase": "TYPE ALIMENTATION",
          "raw_label_titlecase": "Type alimentation",
          "disambiguation_number": null,
          "label": "type alimentation",
          "label_lowercase": "type alimentation",
          "label_uppercase": "TYPE ALIMENTATION",
          "label_titlecase": "Type alimentation",
          "primary": false,
          "nature": "deleted_child_discriminant_",
          "data_type": "INTEGER UNSIGNED NOT NULL",
          "association_name": " <= ANIMAL,CARNIVORE,HERBIVORE",
          "association_name_lower_case": " <= animal,carnivore,herbivore",
          "association_name_uppercase": " <= ANIMAL,CARNIVORE,HERBIVORE",
          "association_name_titlecase": " <= animal,carnivore,herbivore",
          "leg_note": null,
          "outer_source": null,
          "outer_source_lowercase": null,
          "outer_source_uppercase": null,
          "outer_source_titlecase": null
        },
        {
          "attribute": "CARNIVORE",
          "raw_label": "CARNIVORE",
          "raw_label_lowercase": "carnivore",
          "raw_label_uppercase": "CARNIVORE",
          "raw_label_titlecase": "Carnivore",
          "disambiguation_number": null,
          "label": "CARNIVORE",
          "label_lowercase": "carnivore",
          "label_uppercase": "CARNIVORE",
          "label_titlecase": "Carnivore",
          "primary": false,
          "nature": "deleted_child_entity_name",
          "data_type": "BOOLEAN",
          "association_name": " <= ANIMAL,CARNIVORE,HERBIVORE",
          "association_name_lower_case": " <= animal,carnivore,herbivore",
          "association_name_uppercase": " <= ANIMAL,CARNIVORE,HERBIVORE",
          "association_name_titlecase": " <= animal,carnivore,herbivore",
          "leg_note": null,
          "outer_source": "CARNIVORE",
          "outer_source_lowercase": "carnivore",
          "outer_source_uppercase": "CARNIVORE",
          "outer_source_titlecase": "Carnivore"
        },
        {
          "attribute": "quantité viande",
          "raw_label": "quantité viande",
          "raw_label_lowercase": "quantité viande",
          "raw_label_uppercase": "QUANTITÉ VIANDE",
          "raw_label_titlecase": "Quantité viande",
          "disambiguation_number": null,
          "label": "quantité viande",
          "label_lowercase": "quantité viande",
          "label_uppercase": "QUANTITÉ VIANDE",
          "label_titlecase": "Quantité viande",
          "primary": false,
          "nature": "deleted_child_attribute",
          "data_type": null,
          "association_name": " <= ANIMAL,CARNIVORE,HERBIVORE",
          "association_name_lower_case": " <= animal,carnivore,herbivore",
          "association_name_uppercase": " <= ANIMAL,CARNIVORE,HERBIVORE",
          "association_name_titlecase": " <= animal,carnivore,herbivore",
          "leg_note": null,
          "outer_source": null,
          "outer_source_lowercase": null,
          "outer_source_uppercase": null,
          "outer_source_titlecase": null
        },
        {
          "attribute": "HERBIVORE",
          "raw_label": "HERBIVORE",
          "raw_label_lowercase": "herbivore",
          "raw_label_uppercase": "HERBIVORE",
          "raw_label_titlecase": "Herbivore",
          "disambiguation_number": null,
          "label": "HERBIVORE",
          "label_lowercase": "herbivore",
          "label_uppercase": "HERBIVORE",
          "label_titlecase": "Herbivore",
          "primary": false,
          "nature": "deleted_child_entity_name",
          "data_type": "BOOLEAN",
          "association_name": " <= ANIMAL,CARNIVORE,HERBIVORE",
          "association_name_lower_case": " <= animal,carnivore,herbivore",
          "association_name_uppercase": " <= ANIMAL,CARNIVORE,HERBIVORE",
          "association_name_titlecase": " <= animal,carnivore,herbivore",
          "leg_note": null,
          "outer_source": "HERBIVORE",
          "outer_source_lowercase": "herbivore",
          "outer_source_uppercase": "HERBIVORE",
          "outer_source_titlecase": "Herbivore"
        },
        {
          "attribute": "plante préférée",
          "raw_label": "plante préférée",
          "raw_label_lowercase": "plante préférée",
          "raw_label_uppercase": "PLANTE PRÉFÉRÉE",
          "raw_label_titlecase": "Plante préférée",
          "disambiguation_number": null,
          "label": "plante préférée",
          "label_lowercase": "plante préférée",
          "label_uppercase": "PLANTE PRÉFÉRÉE",
          "label_titlecase": "Plante préférée",
          "primary": false,
          "nature": "deleted_child_attribute",
          "data_type": null,
          "association_name": " <= ANIMAL,CARNIVORE,HERBIVORE",
          "association_name_lower_case": " <= animal,carnivore,herbivore",
          "association_name_uppercase": " <= ANIMAL,CARNIVORE,HERBIVORE",
          "association_name_titlecase": " <= animal,carnivore,herbivore",
          "leg_note": null,
          "outer_source": null,
          "outer_source_lowercase": null,
          "outer_source_uppercase": null,
          "outer_source_titlecase": null
        }
      ]
    },
    {
      "this_relation_name": "ESPÈCE",
      "this_relation_name_lowercase": "espèce",
      "this_relation_name_uppercase": "ESPÈCE",
      "this_relation_name_titlecase": "Espèce",
      "is_forced": "False",
      "columns": [
        {
          "attribute": "code espèce",
          "raw_label": "code espèce",
          "raw_label_lowercase": "code espèce",
          "raw_label_uppercase": "CODE ESPÈCE",
          "raw_label_titlecase": "Code espèce",
          "disambiguation_number": null,
          "label": "code espèce",
          "label_lowercase": "code espèce",
          "label_uppercase": "CODE ESPÈCE",
          "label_titlecase": "Code espèce",
          "primary": true,
          "nature": "primary_key",
          "data_type": null,
          "association_name": null,
          "association_name_lower_case": null,
          "association_name_uppercase": null,
          "association_name_titlecase": null,
          "leg_note": null,
          "outer_source": null,
          "outer_source_lowercase": null,
          "outer_source_uppercase": null,
          "outer_source_titlecase": null
        },
        {
          "attribute": "libellé",
          "raw_label": "libellé",
          "raw_label_lowercase": "libellé",
          "raw_label_uppercase": "LIBELLÉ",
          "raw_label_titlecase": "Libellé",
          "disambiguation_number": null,
          "label": "libellé",
          "label_lowercase": "libellé",
          "label_uppercase": "LIBELLÉ",
          "label_titlecase": "Libellé",
          "primary": false,
          "nature": "normal_attribute",
          "data_type": null,
          "association_name": null,
          "association_name_lower_case": null,
          "association_name_uppercase": null,
          "association_name_titlecase": null,
          "leg_note": null,
          "outer_source": null,
          "outer_source_lowercase": null,
          "outer_source_uppercase": null,
          "outer_source_titlecase": null
        }
      ]
    },
    {
      "this_relation_name": "OCCUPE",
      "this_relation_name_lowercase": "occupe",
      "this_relation_name_uppercase": "OCCUPE",
      "this_relation_name_titlecase": "Occupe",
      "is_forced": "False",
      "columns": [
        {
          "attribute": "code espèce",
          "raw_label": "code espèce",
          "raw_label_lowercase": "code espèce",
          "raw_label_uppercase": "CODE ESPÈCE",
          "raw_label_titlecase": "Code espèce",
          "disambiguation_number": null,
          "label": "code espèce",
          "label_lowercase": "code espèce",
          "label_uppercase": "CODE ESPÈCE",
          "label_titlecase": "Code espèce",
          "primary": true,
          "nature": "primary_foreign_key",
          "data_type": null,
          "association_name": "OCCUPE",
          "association_name_lower_case": "occupe",
          "association_name_uppercase": "OCCUPE",
          "association_name_titlecase": "Occupe",
          "leg_note": null,
          "outer_source": "ANIMAL",
          "outer_source_lowercase": "animal",
          "outer_source_uppercase": "ANIMAL",
          "outer_source_titlecase": "Animal"
        },
        {
          "attribute": "nom",
          "raw_label": "nom",
          "raw_label_lowercase": "nom",
          "raw_label_uppercase": "NOM",
          "raw_label_titlecase": "Nom",
          "disambiguation_number": null,
          "label": "nom",
          "label_lowercase": "nom",
          "label_uppercase": "NOM",
          "label_titlecase": "Nom",
          "primary": true,
          "nature": "primary_foreign_key",
          "data_type": null,
          "association_name": "OCCUPE",
          "association_name_lower_case": "occupe",
          "association_name_uppercase": "OCCUPE",
          "association_name_titlecase": "Occupe",
          "leg_note": null,
          "outer_source": "ANIMAL",
          "outer_source_lowercase": "animal",
          "outer_source_uppercase": "ANIMAL",
          "outer_source_titlecase": "Animal"
        },
        {
          "attribute": "num. enclos",
          "raw_label": "num. enclos",
          "raw_label_lowercase": "num. enclos",
          "raw_label_uppercase": "NUM. ENCLOS",
          "raw_label_titlecase": "Num. enclos",
          "disambiguation_number": null,
          "label": "num. enclos",
          "label_lowercase": "num. enclos",
          "label_uppercase": "NUM. ENCLOS",
          "label_titlecase": "Num. enclos",
          "primary": true,
          "nature": "primary_naturalized_foreign_key",
          "data_type": null,
          "association_name": "OCCUPE",
          "association_name_lower_case": "occupe",
          "association_name_uppercase": "OCCUPE",
          "association_name_titlecase": "Occupe",
          "leg_note": null,
          "outer_source": "ENCLOS",
          "outer_source_lowercase": "enclos",
          "outer_source_uppercase": "ENCLOS",
          "outer_source_titlecase": "Enclos"
        },
        {
          "attribute": "date début",
          "raw_label": "date début",
          "raw_label_lowercase": "date début",
          "raw_label_uppercase": "DATE DÉBUT",
          "raw_label_titlecase": "Date début",
          "disambiguation_number": null,
          "label": "date début",
          "label_lowercase": "date début",
          "label_uppercase": "DATE DÉBUT",
          "label_titlecase": "Date début",
          "primary": false,
          "nature": "demoted_naturalized_foreign_key",
          "data_type": null,
          "association_name": "OCCUPE",
          "association_name_lower_case": "occupe",
          "association_name_uppercase": "OCCUPE",
          "association_name_titlecase": "Occupe",
          "leg_note": null,
          "outer_source": "PÉRIODE",
          "outer_source_lowercase": "période",
          "outer_source_uppercase": "PÉRIODE",
          "outer_source_titlecase": "Période"
        },
        {
          "attribute": "date fin",
          "raw_label": "date fin",
          "raw_label_lowercase": "date fin",
          "raw_label_uppercase": "DATE FIN",
          "raw_label_titlecase": "Date fin",
          "disambiguation_number": null,
          "label": "date fin",
          "label_lowercase": "date fin",
          "label_uppercase": "DATE FIN",
          "label_titlecase": "Date fin",
          "primary": false,
          "nature": "demoted_naturalized_foreign_key",
          "data_type": null,
          "association_name": "OCCUPE",
          "association_name_lower_case": "occupe",
          "association_name_uppercase": "OCCUPE",
          "association_name_titlecase": "Occupe",
          "leg_note": null,
          "outer_source": "PÉRIODE",
          "outer_source_lowercase": "période",
          "outer_source_uppercase": "PÉRIODE",
          "outer_source_titlecase": "Période"
        }
      ]
    },
    {
      "this_relation_name": "PEUT COHABITER AVEC",
      "this_relation_name_lowercase": "peut cohabiter avec",
      "this_relation_name_uppercase": "PEUT COHABITER AVEC",
      "this_relation_name_titlecase": "Peut cohabiter avec",
      "is_forced": "False",
      "columns": [
        {
          "attribute": "code espèce",
          "raw_label": "code espèce",
          "raw_label_lowercase": "code espèce",
          "raw_label_uppercase": "CODE ESPÈCE",
          "raw_label_titlecase": "Code espèce",
          "disambiguation_number": null,
          "label": "code espèce",
          "label_lowercase": "code espèce",
          "label_uppercase": "CODE ESPÈCE",
          "label_titlecase": "Code espèce",
          "primary": true,
          "nature": "primary_foreign_key",
          "data_type": null,
          "association_name": "PEUT COHABITER AVEC",
          "association_name_lower_case": "peut cohabiter avec",
          "association_name_uppercase": "PEUT COHABITER AVEC",
          "association_name_titlecase": "Peut cohabiter avec",
          "leg_note": null,
          "outer_source": "ESPÈCE",
          "outer_source_lowercase": "espèce",
          "outer_source_uppercase": "ESPÈCE",
          "outer_source_titlecase": "Espèce"
        },
        {
          "attribute": "code espèce",
          "raw_label": "code espèce",
          "raw_label_lowercase": "code espèce",
          "raw_label_uppercase": "CODE ESPÈCE",
          "raw_label_titlecase": "Code espèce",
          "disambiguation_number": null,
          "label": "code espèce commensale",
          "label_lowercase": "code espèce commensale",
          "label_uppercase": "CODE ESPÈCE COMMENSALE",
          "label_titlecase": "Code espèce commensale",
          "primary": true,
          "nature": "primary_foreign_key",
          "data_type": null,
          "association_name": "PEUT COHABITER AVEC",
          "association_name_lower_case": "peut cohabiter avec",
          "association_name_uppercase": "PEUT COHABITER AVEC",
          "association_name_titlecase": "Peut cohabiter avec",
          "leg_note": "commensale",
          "outer_source": "ESPÈCE",
          "outer_source_lowercase": "espèce",
          "outer_source_uppercase": "ESPÈCE",
          "outer_source_titlecase": "Espèce"
        },
        {
          "attribute": "nb. max. commensaux",
          "raw_label": "nb. max. commensaux",
          "raw_label_lowercase": "nb. max. commensaux",
          "raw_label_uppercase": "NB. MAX. COMMENSAUX",
          "raw_label_titlecase": "Nb. max. commensaux",
          "disambiguation_number": null,
          "label": "nb. max. commensaux",
          "label_lowercase": "nb. max. commensaux",
          "label_uppercase": "NB. MAX. COMMENSAUX",
          "label_titlecase": "Nb. max. commensaux",
          "primary": false,
          "nature": "association_attribute",
          "data_type": null,
          "association_name": "PEUT COHABITER AVEC",
          "association_name_lower_case": "peut cohabiter avec",
          "association_name_uppercase": "PEUT COHABITER AVEC",
          "association_name_titlecase": "Peut cohabiter avec",
          "leg_note": null,
          "outer_source": null,
          "outer_source_lowercase": null,
          "outer_source_uppercase": null,
          "outer_source_titlecase": null
        }
      ]
    },
    {
      "this_relation_name": "PEUT VIVRE DANS",
      "this_relation_name_lowercase": "peut vivre dans",
      "this_relation_name_uppercase": "PEUT VIVRE DANS",
      "this_relation_name_titlecase": "Peut vivre dans",
      "is_forced": "False",
      "columns": [
        {
          "attribute": "code espèce",
          "raw_label": "code espèce",
          "raw_label_lowercase": "code espèce",
          "raw_label_uppercase": "CODE ESPÈCE",
          "raw_label_titlecase": "Code espèce",
          "disambiguation_number": null,
          "label": "code espèce",
          "label_lowercase": "code espèce",
          "label_uppercase": "CODE ESPÈCE",
          "label_titlecase": "Code espèce",
          "primary": true,
          "nature": "primary_foreign_key",
          "data_type": null,
          "association_name": "PEUT VIVRE DANS",
          "association_name_lower_case": "peut vivre dans",
          "association_name_uppercase": "PEUT VIVRE DANS",
          "association_name_titlecase": "Peut vivre dans",
          "leg_note": null,
          "outer_source": "ESPÈCE",
          "outer_source_lowercase": "espèce",
          "outer_source_uppercase": "ESPÈCE",
          "outer_source_titlecase": "Espèce"
        },
        {
          "attribute": "num. enclos",
          "raw_label": "num. enclos",
          "raw_label_lowercase": "num. enclos",
          "raw_label_uppercase": "NUM. ENCLOS",
          "raw_label_titlecase": "Num. enclos",
          "disambiguation_number": null,
          "label": "num. enclos",
          "label_lowercase": "num. enclos",
          "label_uppercase": "NUM. ENCLOS",
          "label_titlecase": "Num. enclos",
          "primary": true,
          "nature": "primary_naturalized_foreign_key",
          "data_type": null,
          "association_name": "PEUT VIVRE DANS",
          "association_name_lower_case": "peut vivre dans",
          "association_name_uppercase": "PEUT VIVRE DANS",
          "association_name_titlecase": "Peut vivre dans",
          "leg_note": null,
          "outer_source": "ENCLOS",
          "outer_source_lowercase": "enclos",
          "outer_source_uppercase": "ENCLOS",
          "outer_source_titlecase": "Enclos"
        },
        {
          "attribute": "nb. max. congénères",
          "raw_label": "nb. max. congénères",
          "raw_label_lowercase": "nb. max. congénères",
          "raw_label_uppercase": "NB. MAX. CONGÉNÈRES",
          "raw_label_titlecase": "Nb. max. congénères",
          "disambiguation_number": null,
          "label": "nb. max. congénères",
          "label_lowercase": "nb. max. congénères",
          "label_uppercase": "NB. MAX. CONGÉNÈRES",
          "label_titlecase": "Nb. max. congénères",
          "primary": false,
          "nature": "association_attribute",
          "data_type": null,
          "association_name": "PEUT VIVRE DANS",
          "association_name_lower_case": "peut vivre dans",
          "association_name_uppercase": "PEUT VIVRE DANS",
          "association_name_titlecase": "Peut vivre dans",
          "leg_note": null,
          "outer_source": null,
          "outer_source_lowercase": null,
          "outer_source_uppercase": null,
          "outer_source_titlecase": null
        }
      ]
    }
  ]
}
```

### `latex.json`

```latex
% Copy this before \begin{document}

\usepackage[normalem]{ulem}
\newenvironment{mld}
  {\par\begin{minipage}{\linewidth}\begin{tabular}{rp{0.7\linewidth}}}
  {\end{tabular}\end{minipage}\par}
\newcommand{\relat}[1]{\textsc{#1}}
\newcommand{\attr}[1]{\emph{#1}}
\newcommand{\prim}[1]{\uline{#1}}
\newcommand{\foreign}[1]{\#\textsl{#1}}

% Copy that after \begin{document}

\begin{mld}
  Animal & (\foreign{\prim{code espèce}}, \prim{nom}, \attr{sexe}, \attr{date naissance}, \attr{date décès}, \foreign{code espèce mère}, \foreign{nom mère}, \attr{type alimentation}, \attr{CARNIVORE}, \attr{quantité viande}, \attr{HERBIVORE}, \attr{plante préférée})\\
  Espèce & (\prim{code espèce}, \attr{libellé})\\
  Occupe & (\foreign{\prim{code espèce}}, \foreign{\prim{nom}}, \prim{num. enclos}, \attr{date début}, \attr{date fin})\\
  Peut cohabiter avec & (\foreign{\prim{code espèce}}, \foreign{\prim{code espèce commensale}}, \attr{nb. max. commensaux})\\
  Peut vivre dans & (\foreign{\prim{code espèce}}, \prim{num. enclos}, \attr{nb. max. congénères})\\
\end{mld}
```

### `latex_without_def.json`

```latex
\begin{mld}
  Animal & (\foreign{\prim{code espèce}}, \prim{nom}, \attr{sexe}, \attr{date naissance}, \attr{date décès}, \foreign{code espèce mère}, \foreign{nom mère}, \attr{type alimentation}, \attr{CARNIVORE}, \attr{quantité viande}, \attr{HERBIVORE}, \attr{plante préférée})\\
  Espèce & (\prim{code espèce}, \attr{libellé})\\
  Occupe & (\foreign{\prim{code espèce}}, \foreign{\prim{nom}}, \prim{num. enclos}, \attr{date début}, \attr{date fin})\\
  Peut cohabiter avec & (\foreign{\prim{code espèce}}, \foreign{\prim{code espèce commensale}}, \attr{nb. max. commensaux})\\
  Peut vivre dans & (\foreign{\prim{code espèce}}, \prim{num. enclos}, \attr{nb. max. congénères})\\
\end{mld}
```

### `markdown.json`

```markdown
**ANIMAL** (<ins>_#code espèce_</ins>, <ins>nom</ins>, sexe, date naissance, date décès, _#code espèce mère_, _#nom mère_, type alimentation, CARNIVORE, quantité viande, HERBIVORE, plante préférée)<br>
**ESPÈCE** (<ins>code espèce</ins>, libellé)<br>
**OCCUPE** (<ins>_#code espèce_</ins>, <ins>_#nom_</ins>, <ins>num. enclos</ins>, date début, date fin)<br>
**PEUT COHABITER AVEC** (<ins>_#code espèce_</ins>, <ins>_#code espèce commensale_</ins>, nb. max. commensaux)<br>
**PEUT VIVRE DANS** (<ins>_#code espèce_</ins>, <ins>num. enclos</ins>, nb. max. congénères)
```

### `markdown_data_dict.json`

```markdown
- nom
- sexe
- date naissance
- date décès
- type alimentation : _INTEGER UNSIGNED NOT NULL_
- CARNIVORE : _BOOLEAN_
- quantité viande
- HERBIVORE : _BOOLEAN_
- plante préférée
- code espèce
- libellé
- num. enclos
- date début
- date fin
- nb. max. commensaux
- num. enclos
- nb. max. congénères
```

### `markdown_verbose.json`

```markdown
**ANIMAL** (<ins>_#code espèce_</ins>, <ins>nom</ins>, sexe, date naissance, date décès, _#code espèce mère_, _#nom mère_, type alimentation, CARNIVORE, quantité viande, HERBIVORE, plante préférée)  
- Le champ _code espèce_ fait partie de la clé primaire de la table. Il a migré à partir de l'entité _ESPÈCE_ pour renforcer l'identifiant.  
- Le champ _nom_ fait partie de la clé primaire de la table. C'était déjà un identifiant de l'entité _ANIMAL_.  
- Les champs _sexe_, _date naissance_ et _date décès_ étaient déjà de simples attributs de l'entité _ANIMAL_.  
- Le champ _code espèce mère_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _A MÈRE_ à partir de l'entité _ANIMAL_ en perdant son caractère identifiant.  
- Le champ _nom mère_ est une clé étrangère. Il a migré par l'association de dépendance fonctionnelle _A MÈRE_ à partir de l'entité _ANIMAL_ en perdant son caractère identifiant.  
- Un champ entier _type alimentation_ est ajouté pour indiquer la nature de la spécialisation. Il est interprété comme un code binaire : bit 1 pour la première entité-fille, bit 2 pour la deuxième, etc. Peut être vide, du fait de l'absence de contrainte de totalité.  
- Un champ booléen _CARNIVORE_ est ajouté pour indiquer si on a affaire ou pas à la spécialisation de même nom.  
- Le champ _quantité viande_ a migré à partir de l'entité-fille _CARNIVORE_ (supprimée).  
- Un champ booléen _HERBIVORE_ est ajouté pour indiquer si on a affaire ou pas à la spécialisation de même nom.  
- Le champ _plante préférée_ a migré à partir de l'entité-fille _HERBIVORE_ (supprimée).  

**ESPÈCE** (<ins>code espèce</ins>, libellé)  
- Le champ _code espèce_ constitue la clé primaire de la table. C'était déjà un identifiant de l'entité _ESPÈCE_.  
- Le champ _libellé_ était déjà un simple attribut de l'entité _ESPÈCE_.  

**OCCUPE** (<ins>_#code espèce_</ins>, <ins>_#nom_</ins>, <ins>_#num. enclos_</ins>, _#date début_, _#date fin_)  
- Les champs _code espèce_ et _nom_ font partie de la clé primaire de la table. Ce sont des clés étrangères qui ont migré directement à partir de l'entité _ANIMAL_.  
- Le champ _num. enclos_ fait partie de la clé primaire de la table. Sa table d'origine (_ENCLOS_) ayant été supprimée, il n'est pas considéré comme clé étrangère.  
- Le champ _date début_ est un simple attribut. Sa table d'origine, _PÉRIODE_, ayant été supprimée, il n'est pas considéré comme clé étrangère. Il devrait normalement faire partie de l'identifiant de _OCCUPE_, mais a été rétrogradé explicitement au rang de simple attribut.  
- Le champ _date fin_ est un simple attribut. Sa table d'origine, _PÉRIODE_, ayant été supprimée, il n'est pas considéré comme clé étrangère. Il devrait normalement faire partie de l'identifiant de _OCCUPE_, mais a été rétrogradé explicitement au rang de simple attribut.  

**PEUT COHABITER AVEC** (<ins>_#code espèce_</ins>, <ins>_#code espèce commensale_</ins>, nb. max. commensaux)  
- Les champs _code espèce_ et _code espèce commensale_ constituent la clé primaire de la table. Ce sont des clés étrangères qui ont migré directement à partir de l'entité _ESPÈCE_.  
- Le champ _nb. max. commensaux_ était déjà un simple attribut de l'association _PEUT COHABITER AVEC_.  

**PEUT VIVRE DANS** (<ins>_#code espèce_</ins>, <ins>_#num. enclos_</ins>, nb. max. congénères)  
- Le champ _code espèce_ fait partie de la clé primaire de la table. C'est une clé étrangère qui a migré directement à partir de l'entité _ESPÈCE_.  
- Le champ _num. enclos_ fait partie de la clé primaire de la table. Sa table d'origine (_ENCLOS_) ayant été supprimée, il n'est pas considéré comme clé étrangère.  
- Le champ _nb. max. congénères_ était déjà un simple attribut de l'association _PEUT VIVRE DANS_.  

---

**NB.** Les tables _ENCLOS_ et _PÉRIODE_ ont été supprimées car elles étaient réduites à la clé primaire de leur entité d'origine.
```

### `mysql.json`

```sql
CREATE DATABASE IF NOT EXISTS `UNTITLED` DEFAULT CHARACTER SET UTF8MB4 COLLATE utf8_general_ci;
USE `UNTITLED`;

CREATE TABLE `ANIMAL` (
  `code_espèce` VARCHAR(42),
  `nom` VARCHAR(42),
  `sexe` VARCHAR(42),
  `date_naissance` VARCHAR(42),
  `date_décès` VARCHAR(42),
  `code_espèce mère` VARCHAR(42),
  `nom mère` VARCHAR(42),
  `type_alimentation` TINYINT UNSIGNED NOT NULL,
  `carnivore` BOOLEAN,
  `quantité_viande` VARCHAR(42),
  `herbivore` BOOLEAN,
  `plante_préférée` VARCHAR(42),
  PRIMARY KEY (`code_espèce`, `nom`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE `ESPÈCE` (
  `code_espèce` VARCHAR(42),
  `libellé` VARCHAR(42),
  PRIMARY KEY (`code_espèce`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE `OCCUPE` (
  `code_espèce` VARCHAR(42),
  `nom` VARCHAR(42),
  `num_enclos` VARCHAR(42),
  `date_début` VARCHAR(42),
  `date_fin` VARCHAR(42),
  PRIMARY KEY (`code_espèce`, `nom`, `num_enclos`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE `PEUT_COHABITER_AVEC` (
  `code_espèce` VARCHAR(42),
  `code_espèce commensale` VARCHAR(42),
  `nb_max_commensaux` VARCHAR(42),
  PRIMARY KEY (`code_espèce`, `code_espèce commensale`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

CREATE TABLE `PEUT_VIVRE_DANS` (
  `code_espèce` VARCHAR(42),
  `num_enclos` VARCHAR(42),
  `nb_max_congénères` VARCHAR(42),
  PRIMARY KEY (`code_espèce`, `num_enclos`)
) ENGINE=InnoDB DEFAULT CHARSET=UTF8MB4;

ALTER TABLE `ANIMAL` ADD FOREIGN KEY (`code_espèce mère`, `nom mère`) REFERENCES `ANIMAL` (`code_espèce`, `nom`);
ALTER TABLE `ANIMAL` ADD FOREIGN KEY (`code_espèce`) REFERENCES `ESPÈCE` (`code_espèce`);
ALTER TABLE `OCCUPE` ADD FOREIGN KEY (`code_espèce`, `nom`) REFERENCES `ANIMAL` (`code_espèce`, `nom`);
ALTER TABLE `PEUT_COHABITER_AVEC` ADD FOREIGN KEY (`code_espèce commensale`) REFERENCES `ESPÈCE` (`code_espèce`);
ALTER TABLE `PEUT_COHABITER_AVEC` ADD FOREIGN KEY (`code_espèce`) REFERENCES `ESPÈCE` (`code_espèce`);
ALTER TABLE `PEUT_VIVRE_DANS` ADD FOREIGN KEY (`code_espèce`) REFERENCES `ESPÈCE` (`code_espèce`);
```

### `oracle.json`

```sql
CREATE TABLE "ANIMAL" (
  "code_espèce" VARCHAR(42),
  "nom" VARCHAR(42),
  "sexe" VARCHAR(42),
  "date_naissance" VARCHAR(42),
  "date_décès" VARCHAR(42),
  "code_espèce mère" VARCHAR(42),
  "nom mère" VARCHAR(42),
  "type_alimentation" NUMBER(1) UNSIGNED NOT NULL,
  "carnivore" NUMBER(1) DEFAULT 0 NOT NULL,
  "quantité_viande" VARCHAR(42),
  "herbivore" NUMBER(1) DEFAULT 0 NOT NULL,
  "plante_préférée" VARCHAR(42),
  PRIMARY KEY ("code_espèce", "nom")
);

CREATE TABLE "ESPÈCE" (
  "code_espèce" VARCHAR(42),
  "libellé" VARCHAR(42),
  PRIMARY KEY ("code_espèce")
);

CREATE TABLE "OCCUPE" (
  "code_espèce" VARCHAR(42),
  "nom" VARCHAR(42),
  "num_enclos" VARCHAR(42),
  "date_début" VARCHAR(42),
  "date_fin" VARCHAR(42),
  PRIMARY KEY ("code_espèce", "nom", "num_enclos")
);

CREATE TABLE "PEUT_COHABITER_AVEC" (
  "code_espèce" VARCHAR(42),
  "code_espèce commensale" VARCHAR(42),
  "nb_max_commensaux" VARCHAR(42),
  PRIMARY KEY ("code_espèce", "code_espèce commensale")
);

CREATE TABLE "PEUT_VIVRE_DANS" (
  "code_espèce" VARCHAR(42),
  "num_enclos" VARCHAR(42),
  "nb_max_congénères" VARCHAR(42),
  PRIMARY KEY ("code_espèce", "num_enclos")
);

ALTER TABLE "ANIMAL" ADD FOREIGN KEY ("code_espèce mère", "nom mère") REFERENCES "ANIMAL" ("code_espèce", "nom");
ALTER TABLE "ANIMAL" ADD FOREIGN KEY ("code_espèce") REFERENCES "ESPÈCE" ("code_espèce");
ALTER TABLE "OCCUPE" ADD FOREIGN KEY ("code_espèce", "nom") REFERENCES "ANIMAL" ("code_espèce", "nom");
ALTER TABLE "PEUT_COHABITER_AVEC" ADD FOREIGN KEY ("code_espèce commensale") REFERENCES "ESPÈCE" ("code_espèce");
ALTER TABLE "PEUT_COHABITER_AVEC" ADD FOREIGN KEY ("code_espèce") REFERENCES "ESPÈCE" ("code_espèce");
ALTER TABLE "PEUT_VIVRE_DANS" ADD FOREIGN KEY ("code_espèce") REFERENCES "ESPÈCE" ("code_espèce");
```

### `postgresql.json`

```sql
CREATE DATABASE UNTITLED;
\c UNTITLED;

CREATE TABLE ANIMAL (
  code_espèce VARCHAR(42),
  nom VARCHAR(42),
  sexe VARCHAR(42),
  date_naissance VARCHAR(42),
  date_décès VARCHAR(42),
  code_espèce mère VARCHAR(42),
  nom mère VARCHAR(42),
  type_alimentation SMALLINT NOT NULL,
  carnivore BOOLEAN,
  quantité_viande VARCHAR(42),
  herbivore BOOLEAN,
  plante_préférée VARCHAR(42),
  PRIMARY KEY (code_espèce, nom)
);

CREATE TABLE ESPÈCE (
  code_espèce VARCHAR(42),
  libellé VARCHAR(42),
  PRIMARY KEY (code_espèce)
);

CREATE TABLE OCCUPE (
  code_espèce VARCHAR(42),
  nom VARCHAR(42),
  num_enclos VARCHAR(42),
  date_début VARCHAR(42),
  date_fin VARCHAR(42),
  PRIMARY KEY (code_espèce, nom, num_enclos)
);

CREATE TABLE PEUT_COHABITER_AVEC (
  code_espèce VARCHAR(42),
  code_espèce commensale VARCHAR(42),
  nb_max_commensaux VARCHAR(42),
  PRIMARY KEY (code_espèce, code_espèce commensale)
);

CREATE TABLE PEUT_VIVRE_DANS (
  code_espèce VARCHAR(42),
  num_enclos VARCHAR(42),
  nb_max_congénères VARCHAR(42),
  PRIMARY KEY (code_espèce, num_enclos)
);

ALTER TABLE ANIMAL ADD FOREIGN KEY (code_espèce mère, nom mère) REFERENCES ANIMAL (code_espèce, nom);
ALTER TABLE ANIMAL ADD FOREIGN KEY (code_espèce) REFERENCES ESPÈCE (code_espèce);
ALTER TABLE OCCUPE ADD FOREIGN KEY (code_espèce, nom) REFERENCES ANIMAL (code_espèce, nom);
ALTER TABLE PEUT_COHABITER_AVEC ADD FOREIGN KEY (code_espèce commensale) REFERENCES ESPÈCE (code_espèce);
ALTER TABLE PEUT_COHABITER_AVEC ADD FOREIGN KEY (code_espèce) REFERENCES ESPÈCE (code_espèce);
ALTER TABLE PEUT_VIVRE_DANS ADD FOREIGN KEY (code_espèce) REFERENCES ESPÈCE (code_espèce);
```

### `sqlite.json`

```sql
.open "UNTITLED";

CREATE TABLE "ANIMAL" (
  "code_espèce" VARCHAR(42),
  "nom" VARCHAR(42),
  "sexe" VARCHAR(42),
  "date_naissance" VARCHAR(42),
  "date_décès" VARCHAR(42),
  "code_espèce mère" VARCHAR(42),
  "nom mère" VARCHAR(42),
  "type_alimentation" INTEGER NOT NULL,
  "carnivore" INTEGER,
  "quantité_viande" VARCHAR(42),
  "herbivore" INTEGER,
  "plante_préférée" VARCHAR(42),
  PRIMARY KEY ("code_espèce", "nom"),
  FOREIGN KEY ("code_espèce") REFERENCES "ESPÈCE" ("code_espèce"),
  FOREIGN KEY ("code_espèce mère", "nom mère") REFERENCES "ANIMAL" ("code_espèce", "nom")
);

CREATE TABLE "ESPÈCE" (
  "code_espèce" VARCHAR(42),
  "libellé" VARCHAR(42),
  PRIMARY KEY ("code_espèce")
);

CREATE TABLE "OCCUPE" (
  "code_espèce" VARCHAR(42),
  "nom" VARCHAR(42),
  "num_enclos" VARCHAR(42),
  "date_début" VARCHAR(42),
  "date_fin" VARCHAR(42),
  PRIMARY KEY ("code_espèce", "nom", "num_enclos"),
  FOREIGN KEY ("code_espèce", "nom") REFERENCES "ANIMAL" ("code_espèce", "nom")
);

CREATE TABLE "PEUT_COHABITER_AVEC" (
  "code_espèce" VARCHAR(42),
  "code_espèce commensale" VARCHAR(42),
  "nb_max_commensaux" VARCHAR(42),
  PRIMARY KEY ("code_espèce", "code_espèce commensale"),
  FOREIGN KEY ("code_espèce") REFERENCES "ESPÈCE" ("code_espèce"),
  FOREIGN KEY ("code_espèce commensale") REFERENCES "ESPÈCE" ("code_espèce")
);

CREATE TABLE "PEUT_VIVRE_DANS" (
  "code_espèce" VARCHAR(42),
  "num_enclos" VARCHAR(42),
  "nb_max_congénères" VARCHAR(42),
  PRIMARY KEY ("code_espèce", "num_enclos"),
  FOREIGN KEY ("code_espèce") REFERENCES "ESPÈCE" ("code_espèce")
);
```

### `text.json`

```
ANIMAL (_#code espèce_, _nom_, sexe, date naissance, date décès, #code espèce mère, #nom mère, type alimentation, CARNIVORE, quantité viande, HERBIVORE, plante préférée)
ESPÈCE (_code espèce_, libellé)
OCCUPE (_#code espèce_, _#nom_, _num. enclos_, date début, date fin)
PEUT COHABITER AVEC (_#code espèce_, _#code espèce commensale_, nb. max. commensaux)
PEUT VIVRE DANS (_#code espèce_, _num. enclos_, nb. max. congénères)
```

### `txt2tags.json`

```plain
Untitled
Généré par Mocodo
%%mtime(%c)
%!encoding: utf8
- **ANIMAL** (__#code espèce__, __nom__, sexe, date naissance, date décès, #code espèce mère, #nom mère, type alimentation, CARNIVORE, quantité viande, HERBIVORE, plante préférée)
- **ESPÈCE** (__code espèce__, libellé)
- **OCCUPE** (__#code espèce__, __#nom__, __num. enclos__, date début, date fin)
- **PEUT COHABITER AVEC** (__#code espèce__, __#code espèce commensale__, nb. max. commensaux)
- **PEUT VIVRE DANS** (__#code espèce__, __num. enclos__, nb. max. congénères)
```

## Inheritance stress test

### External associations

```
    SUSCIPIT: orci, lorem
    RHONCUS, 1N TRISTIS, 11 SUSCIPIT
    :
    :
    SODALES: convallis, ipsum
    VITAE, 11 QUAM, 1N SODALES
    QUAM: cras, sed

    CONSEQUAT: fermentum, dederit
    ELIT, 11 TRISTIS, 1N CONSEQUAT
    TRISTIS: magna, vestibulum
    /T\ TRISTIS {arrow} SODALES, NEC, LACUS: type
    NEC: pulvinar, audis
    MOLLIS, 1N CURABITUR, 11 NEC
    CURABITUR: gravida, amor

    DIGNISSIM: tellus, terra
    ALIQUET, 1N TRISTIS, 1N DIGNISSIM
    :
    :
    LACUS: tempor, fugit
    ULTRICES, 1N LIBERO, 1N LACUS
    LIBERO: posuere, lacrima
```

#### Arrow `<=`
```
ALIQUET (_#magna_, _#tellus_)
CONSEQUAT (_fermentum_, dederit)
CURABITUR (_gravida_, amor)
DIGNISSIM (_tellus_, terra)
LIBERO (_posuere_, lacrima)
QUAM (_cras_, sed, #magna)
SUSCIPIT (_orci_, lorem, #magna)
TRISTIS (_magna_, vestibulum, #fermentum, type, SODALES, convallis, ipsum, NEC, pulvinar, audis, #gravida, LACUS, tempor, fugit)
ULTRICES (_#posuere_, _#magna_)
```

| Relation | Attribute | `nature` | `adjacent_source` | `outer_source` |
|---|---|---|---|---|
| ALIQUET | magna | `primary_foreign_key` | TRISTIS | TRISTIS |
| ALIQUET | tellus | `primary_foreign_key` | DIGNISSIM | DIGNISSIM |
| CONSEQUAT | fermentum | `primary_key` | None | None |
| CONSEQUAT | dederit | `normal_attribute` | None | None |
| CURABITUR | gravida | `primary_key` | None | None |
| CURABITUR | amor | `normal_attribute` | None | None |
| DIGNISSIM | tellus | `primary_key` | None | None |
| DIGNISSIM | terra | `normal_attribute` | None | None |
| LIBERO | posuere | `primary_key` | None | None |
| LIBERO | lacrima | `normal_attribute` | None | None |
| QUAM | cras | `primary_key` | None | None |
| QUAM | sed | `normal_attribute` | None | None |
| QUAM | magna | `foreign_key` | SODALES | TRISTIS |
| SUSCIPIT | orci | `primary_key` | None | None |
| SUSCIPIT | lorem | `normal_attribute` | None | None |
| SUSCIPIT | magna | `foreign_key` | TRISTIS | TRISTIS |
| TRISTIS | magna | `primary_key` | None | None |
| TRISTIS | vestibulum | `normal_attribute` | None | None |
| TRISTIS | fermentum | `foreign_key` | CONSEQUAT | CONSEQUAT |
| TRISTIS | type | `deleted_child_discriminant_T` | None | None |
| TRISTIS | SODALES | `deleted_child_entity_name` | SODALES | SODALES |
| TRISTIS | convallis | `deleted_child_attribute` | SODALES | None |
| TRISTIS | ipsum | `deleted_child_attribute` | SODALES | None |
| TRISTIS | NEC | `deleted_child_entity_name` | NEC | NEC |
| TRISTIS | pulvinar | `deleted_child_attribute` | NEC | None |
| TRISTIS | audis | `deleted_child_attribute` | NEC | None |
| TRISTIS | gravida | `deleted_child_foreign_key` | NEC | CURABITUR |
| TRISTIS | LACUS | `deleted_child_entity_name` | LACUS | LACUS |
| TRISTIS | tempor | `deleted_child_attribute` | LACUS | None |
| TRISTIS | fugit | `deleted_child_attribute` | LACUS | None |
| ULTRICES | posuere | `primary_foreign_key` | LIBERO | LIBERO |
| ULTRICES | magna | `primary_foreign_key` | LACUS | TRISTIS |

#### Arrow `<-`
```
ALIQUET (_#magna_, _#tellus_)
CONSEQUAT (_fermentum_, dederit)
CURABITUR (_gravida_, amor)
DIGNISSIM (_tellus_, terra)
LIBERO (_posuere_, lacrima)
QUAM (_cras_, sed, #magna)
SUSCIPIT (_orci_, lorem, #magna)
TRISTIS (_magna_, vestibulum, #fermentum, type, convallis, ipsum, pulvinar, audis, #gravida, tempor, fugit)
ULTRICES (_#posuere_, _#magna_)
```

| Relation | Attribute | `nature` | `adjacent_source` | `outer_source` |
|---|---|---|---|---|
| ALIQUET | magna | `primary_foreign_key` | TRISTIS | TRISTIS |
| ALIQUET | tellus | `primary_foreign_key` | DIGNISSIM | DIGNISSIM |
| CONSEQUAT | fermentum | `primary_key` | None | None |
| CONSEQUAT | dederit | `normal_attribute` | None | None |
| CURABITUR | gravida | `primary_key` | None | None |
| CURABITUR | amor | `normal_attribute` | None | None |
| DIGNISSIM | tellus | `primary_key` | None | None |
| DIGNISSIM | terra | `normal_attribute` | None | None |
| LIBERO | posuere | `primary_key` | None | None |
| LIBERO | lacrima | `normal_attribute` | None | None |
| QUAM | cras | `primary_key` | None | None |
| QUAM | sed | `normal_attribute` | None | None |
| QUAM | magna | `foreign_key` | SODALES | TRISTIS |
| SUSCIPIT | orci | `primary_key` | None | None |
| SUSCIPIT | lorem | `normal_attribute` | None | None |
| SUSCIPIT | magna | `foreign_key` | TRISTIS | TRISTIS |
| TRISTIS | magna | `primary_key` | None | None |
| TRISTIS | vestibulum | `normal_attribute` | None | None |
| TRISTIS | fermentum | `foreign_key` | CONSEQUAT | CONSEQUAT |
| TRISTIS | type | `deleted_child_discriminant_T` | None | None |
| TRISTIS | convallis | `deleted_child_attribute` | SODALES | None |
| TRISTIS | ipsum | `deleted_child_attribute` | SODALES | None |
| TRISTIS | pulvinar | `deleted_child_attribute` | NEC | None |
| TRISTIS | audis | `deleted_child_attribute` | NEC | None |
| TRISTIS | gravida | `deleted_child_foreign_key` | NEC | CURABITUR |
| TRISTIS | tempor | `deleted_child_attribute` | LACUS | None |
| TRISTIS | fugit | `deleted_child_attribute` | LACUS | None |
| ULTRICES | posuere | `primary_foreign_key` | LIBERO | LIBERO |
| ULTRICES | magna | `primary_foreign_key` | LACUS | TRISTIS |

#### Arrow `->`
```
ALIQUET (_#magna_, _#tellus_)
CONSEQUAT (_fermentum_, dederit)
CURABITUR (_gravida_, amor)
DIGNISSIM (_tellus_, terra)
LACUS (_#magna_, tempor, fugit)
LIBERO (_posuere_, lacrima)
NEC (_#magna_, pulvinar, audis, #gravida)
QUAM (_cras_, sed, #magna)
SODALES (_#magna_, convallis, ipsum)
SUSCIPIT (_orci_, lorem, #magna)
TRISTIS (_magna_, vestibulum, #fermentum, type)
ULTRICES (_#posuere_, _#magna_)
```

| Relation | Attribute | `nature` | `adjacent_source` | `outer_source` |
|---|---|---|---|---|
| ALIQUET | magna | `primary_foreign_key` | TRISTIS | TRISTIS |
| ALIQUET | tellus | `primary_foreign_key` | DIGNISSIM | DIGNISSIM |
| CONSEQUAT | fermentum | `primary_key` | None | None |
| CONSEQUAT | dederit | `normal_attribute` | None | None |
| CURABITUR | gravida | `primary_key` | None | None |
| CURABITUR | amor | `normal_attribute` | None | None |
| DIGNISSIM | tellus | `primary_key` | None | None |
| DIGNISSIM | terra | `normal_attribute` | None | None |
| LACUS | magna | `parent_primary_key` | TRISTIS | TRISTIS |
| LACUS | tempor | `normal_attribute` | None | None |
| LACUS | fugit | `normal_attribute` | None | None |
| LIBERO | posuere | `primary_key` | None | None |
| LIBERO | lacrima | `normal_attribute` | None | None |
| NEC | magna | `parent_primary_key` | TRISTIS | TRISTIS |
| NEC | pulvinar | `normal_attribute` | None | None |
| NEC | audis | `normal_attribute` | None | None |
| NEC | gravida | `foreign_key` | CURABITUR | CURABITUR |
| QUAM | cras | `primary_key` | None | None |
| QUAM | sed | `normal_attribute` | None | None |
| QUAM | magna | `foreign_key` | SODALES | SODALES |
| SODALES | magna | `parent_primary_key` | TRISTIS | TRISTIS |
| SODALES | convallis | `normal_attribute` | None | None |
| SODALES | ipsum | `normal_attribute` | None | None |
| SUSCIPIT | orci | `primary_key` | None | None |
| SUSCIPIT | lorem | `normal_attribute` | None | None |
| SUSCIPIT | magna | `foreign_key` | TRISTIS | TRISTIS |
| TRISTIS | magna | `primary_key` | None | None |
| TRISTIS | vestibulum | `normal_attribute` | None | None |
| TRISTIS | fermentum | `foreign_key` | CONSEQUAT | CONSEQUAT |
| TRISTIS | type | `deleted_child_discriminant_T` | None | None |
| ULTRICES | posuere | `primary_foreign_key` | LIBERO | LIBERO |
| ULTRICES | magna | `primary_foreign_key` | LACUS | LACUS |

#### Arrow `=>`
```
ALIQUET (_magna_, _#tellus_, type)
CONSEQUAT (_fermentum_, dederit)
CURABITUR (_gravida_, amor)
DIGNISSIM (_tellus_, terra)
LACUS (_magna_, vestibulum, #fermentum, tempor, fugit)
LIBERO (_posuere_, lacrima)
NEC (_magna_, vestibulum, #fermentum, pulvinar, audis, #gravida)
QUAM (_cras_, sed, #magna)
SODALES (_magna_, vestibulum, #fermentum, convallis, ipsum)
SUSCIPIT (_orci_, lorem, magna, type)
ULTRICES (_#posuere_, _#magna_)
```

| Relation | Attribute | `nature` | `adjacent_source` | `outer_source` |
|---|---|---|---|---|
| ALIQUET | magna | `unsourced_primary_foreign_key` | TRISTIS | None |
| ALIQUET | tellus | `primary_foreign_key` | DIGNISSIM | DIGNISSIM |
| ALIQUET | type | `normal_attribute` | TRISTIS | None |
| CONSEQUAT | fermentum | `primary_key` | None | None |
| CONSEQUAT | dederit | `normal_attribute` | None | None |
| CURABITUR | gravida | `primary_key` | None | None |
| CURABITUR | amor | `normal_attribute` | None | None |
| DIGNISSIM | tellus | `primary_key` | None | None |
| DIGNISSIM | terra | `normal_attribute` | None | None |
| LACUS | magna | `deleted_parent_primary_key` | TRISTIS | TRISTIS |
| LACUS | vestibulum | `deleted_parent_attribute` | TRISTIS | None |
| LACUS | fermentum | `deleted_parent_foreign_key` | TRISTIS | CONSEQUAT |
| LACUS | tempor | `normal_attribute` | None | None |
| LACUS | fugit | `normal_attribute` | None | None |
| LIBERO | posuere | `primary_key` | None | None |
| LIBERO | lacrima | `normal_attribute` | None | None |
| NEC | magna | `deleted_parent_primary_key` | TRISTIS | TRISTIS |
| NEC | vestibulum | `deleted_parent_attribute` | TRISTIS | None |
| NEC | fermentum | `deleted_parent_foreign_key` | TRISTIS | CONSEQUAT |
| NEC | pulvinar | `normal_attribute` | None | None |
| NEC | audis | `normal_attribute` | None | None |
| NEC | gravida | `foreign_key` | CURABITUR | CURABITUR |
| QUAM | cras | `primary_key` | None | None |
| QUAM | sed | `normal_attribute` | None | None |
| QUAM | magna | `foreign_key` | SODALES | SODALES |
| SODALES | magna | `deleted_parent_primary_key` | TRISTIS | TRISTIS |
| SODALES | vestibulum | `deleted_parent_attribute` | TRISTIS | None |
| SODALES | fermentum | `deleted_parent_foreign_key` | TRISTIS | CONSEQUAT |
| SODALES | convallis | `normal_attribute` | None | None |
| SODALES | ipsum | `normal_attribute` | None | None |
| SUSCIPIT | orci | `primary_key` | None | None |
| SUSCIPIT | lorem | `normal_attribute` | None | None |
| SUSCIPIT | magna | `unsourced_foreign_key` | TRISTIS | None |
| SUSCIPIT | type | `normal_attribute` | TRISTIS | None |
| ULTRICES | posuere | `primary_foreign_key` | LIBERO | LIBERO |
| ULTRICES | magna | `primary_foreign_key` | LACUS | LACUS |

### Internal associations

```
:
MOLLIS, 1N [via mollis] LACUS, 11 NEC
NEC: pulvinar, audis
:

LACUS: tempor, fugit
/XT\ TRISTIS {arrow} SODALES, NEC, LACUS: type
TRISTIS: magna, vestibulum
VITAE, 11 NEC, 1N [via vitae] SODALES

:
ULTRICES, 1N [sodales] SODALES, 1N [lacus] LACUS
SODALES: convallis, ipsum
:
```

#### Arrow `<=`
```
TRISTIS (_magna_, vestibulum, type, SODALES, convallis, ipsum, NEC, pulvinar, audis, #magna via mollis, #magna via vitae, LACUS, tempor, fugit)
ULTRICES (_#magna sodales_, _#magna lacus_)
```

| Relation | Attribute | `nature` | `adjacent_source` | `outer_source` |
|---|---|---|---|---|
| TRISTIS | magna | `primary_key` | None | None |
| TRISTIS | vestibulum | `normal_attribute` | None | None |
| TRISTIS | type | `deleted_child_discriminant_XT` | None | None |
| TRISTIS | SODALES | `deleted_child_entity_name` | SODALES | SODALES |
| TRISTIS | convallis | `deleted_child_attribute` | SODALES | None |
| TRISTIS | ipsum | `deleted_child_attribute` | SODALES | None |
| TRISTIS | NEC | `deleted_child_entity_name` | NEC | NEC |
| TRISTIS | pulvinar | `deleted_child_attribute` | NEC | None |
| TRISTIS | audis | `deleted_child_attribute` | NEC | None |
| TRISTIS | magna via mollis | `deleted_child_foreign_key` | NEC | TRISTIS |
| TRISTIS | magna via vitae | `deleted_child_foreign_key` | NEC | TRISTIS |
| TRISTIS | LACUS | `deleted_child_entity_name` | LACUS | LACUS |
| TRISTIS | tempor | `deleted_child_attribute` | LACUS | None |
| TRISTIS | fugit | `deleted_child_attribute` | LACUS | None |
| ULTRICES | magna sodales | `primary_foreign_key` | SODALES | TRISTIS |
| ULTRICES | magna lacus | `primary_foreign_key` | LACUS | TRISTIS |

#### Arrow `<-`
```
TRISTIS (_magna_, vestibulum, type, convallis, ipsum, pulvinar, audis, #magna via mollis, #magna via vitae, tempor, fugit)
ULTRICES (_#magna sodales_, _#magna lacus_)
```

| Relation | Attribute | `nature` | `adjacent_source` | `outer_source` |
|---|---|---|---|---|
| TRISTIS | magna | `primary_key` | None | None |
| TRISTIS | vestibulum | `normal_attribute` | None | None |
| TRISTIS | type | `deleted_child_discriminant_XT` | None | None |
| TRISTIS | convallis | `deleted_child_attribute` | SODALES | None |
| TRISTIS | ipsum | `deleted_child_attribute` | SODALES | None |
| TRISTIS | pulvinar | `deleted_child_attribute` | NEC | None |
| TRISTIS | audis | `deleted_child_attribute` | NEC | None |
| TRISTIS | magna via mollis | `deleted_child_foreign_key` | NEC | TRISTIS |
| TRISTIS | magna via vitae | `deleted_child_foreign_key` | NEC | TRISTIS |
| TRISTIS | tempor | `deleted_child_attribute` | LACUS | None |
| TRISTIS | fugit | `deleted_child_attribute` | LACUS | None |
| ULTRICES | magna sodales | `primary_foreign_key` | SODALES | TRISTIS |
| ULTRICES | magna lacus | `primary_foreign_key` | LACUS | TRISTIS |

#### Arrow `->`
```
LACUS (_#magna_, tempor, fugit)
NEC (_#magna_, pulvinar, audis, #magna via mollis, #magna via vitae)
SODALES (_#magna_, convallis, ipsum)
TRISTIS (_magna_, vestibulum, type)
ULTRICES (_#magna sodales_, _#magna lacus_)
```

| Relation | Attribute | `nature` | `adjacent_source` | `outer_source` |
|---|---|---|---|---|
| LACUS | magna | `parent_primary_key` | TRISTIS | TRISTIS |
| LACUS | tempor | `normal_attribute` | None | None |
| LACUS | fugit | `normal_attribute` | None | None |
| NEC | magna | `parent_primary_key` | TRISTIS | TRISTIS |
| NEC | pulvinar | `normal_attribute` | None | None |
| NEC | audis | `normal_attribute` | None | None |
| NEC | magna via mollis | `foreign_key` | LACUS | LACUS |
| NEC | magna via vitae | `foreign_key` | SODALES | SODALES |
| SODALES | magna | `parent_primary_key` | TRISTIS | TRISTIS |
| SODALES | convallis | `normal_attribute` | None | None |
| SODALES | ipsum | `normal_attribute` | None | None |
| TRISTIS | magna | `primary_key` | None | None |
| TRISTIS | vestibulum | `normal_attribute` | None | None |
| TRISTIS | type | `deleted_child_discriminant_XT` | None | None |
| ULTRICES | magna sodales | `primary_foreign_key` | SODALES | SODALES |
| ULTRICES | magna lacus | `primary_foreign_key` | LACUS | LACUS |

#### Arrow `=>`
```
LACUS (_magna_, vestibulum, tempor, fugit)
NEC (_magna_, vestibulum, pulvinar, audis, #magna via mollis, #magna via vitae)
SODALES (_magna_, vestibulum, convallis, ipsum)
ULTRICES (_#magna sodales_, _#magna lacus_)
```

| Relation | Attribute | `nature` | `adjacent_source` | `outer_source` |
|---|---|---|---|---|
| LACUS | magna | `deleted_parent_primary_key` | TRISTIS | TRISTIS |
| LACUS | vestibulum | `deleted_parent_attribute` | TRISTIS | None |
| LACUS | tempor | `normal_attribute` | None | None |
| LACUS | fugit | `normal_attribute` | None | None |
| NEC | magna | `deleted_parent_primary_key` | TRISTIS | TRISTIS |
| NEC | vestibulum | `deleted_parent_attribute` | TRISTIS | None |
| NEC | pulvinar | `normal_attribute` | None | None |
| NEC | audis | `normal_attribute` | None | None |
| NEC | magna via mollis | `foreign_key` | LACUS | LACUS |
| NEC | magna via vitae | `foreign_key` | SODALES | SODALES |
| SODALES | magna | `deleted_parent_primary_key` | TRISTIS | TRISTIS |
| SODALES | vestibulum | `deleted_parent_attribute` | TRISTIS | None |
| SODALES | convallis | `normal_attribute` | None | None |
| SODALES | ipsum | `normal_attribute` | None | None |
| ULTRICES | magna sodales | `primary_foreign_key` | SODALES | SODALES |
| ULTRICES | magna lacus | `primary_foreign_key` | LACUS | LACUS |
