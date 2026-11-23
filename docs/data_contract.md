# Contrat de données : Bank Marketing

| | |
|---|---|
| **Producteur** | Équipe CRM de la banque |
| **Consommateur** | Pipeline d'entraînement `mlops_projet` |
| **Format** | CSV, séparateur `;`, 17 colonnes |
| **Fréquence** | Un fichier après chaque campagne |
| **Version** | 1.0 |

## Règles

| Colonne | Type | Règle |
|---|---|---|
| age | entier | entre 18 et 100 |
| job, marital, education, contact, month, poutcome | texte | valeur dans la liste connue |
| default, housing, loan, y | texte | `yes` ou `no` |
| day | entier | entre 1 et 31 |
| duration, previous | entier | ≥ 0 |
| campaign | entier | ≥ 1 |
| pdays | entier | ≥ -1 (-1 = jamais contacté) |
| balance | entier | aucune limite (peut être négatif) |

Aucune colonne en plus, aucune en moins. `unknown` est une valeur autorisée.

## Si le contrat n'est pas respecté

Le pipeline s'arrête, on n'entraîne pas, et on prévient le producteur.

Code : `src/mlops_projet/data/schema.py`