# Auteur
👤 Auteur
Abdoulaye Mahamadou Touré

GitHub : https://github.com/abdoulaye1403

Dépôt du projet : https://github.com/abdoulaye1403/finance-etl-analytics

Portfolio : https://abdoulaye1403.github.io/

E-mail : abdelraul140385@gmail.com
# 💳 Pipeline ETL & Analyse de Portefeuille Microfinance (`finance-etl-analytics`)

Ce dépôt contient un pipeline **ETL (Extract, Transform, Load)** en **Python** avec **Pandas** et **NumPy** dédié au nettoyage, à l'enrichissement et au suivi d'un portefeuille de prêts en microfinance (**XOF**).

---

## 🎯 Objectif du projet

Automatiser la préparation et l'analyse des données de prêts afin de produire un jeu de données nettoyé dans `outputs/` et un résumé des indicateurs clés de recouvrement et de risque crédit.

---

## ⚙️ Ce que fait le pipeline (`automatisation_pipeline_data`)

1. **Extraction & contrôle :**
   - Vérifie l'existence du fichier source dans `data/` et charge les données avec `pandas.read_csv()`.

2. **Nettoyage & imputation des valeurs manquantes :**
   - `Secteur_Activite` : remplacement des valeurs manquantes (`NaN`) par `'Non renseigné'`.
   - `Region` : remplacement des valeurs manquantes (`NaN`) par `'Inconnue'`.
   - `Age` : imputation par la médiane de la population et conversion en entier (`int`).
   - Suppression des doublons stricts avec `drop_duplicates()`.

3. **Enrichissement des données (Feature Engineering) :**
   - **`Taux_Remboursement_%`** : pourcentage remboursé par prêt (`Montant_Rembourse_XOF / Montant_Pret_XOF * 100`), arrondi à 1 décimale.
   - **`Reste_A_Rembourser_XOF`** : encours restant dû (`Montant_Pret_XOF - Montant_Rembourse_XOF`).
   - **`Indicateur_PAR90`** : indicateur binaire (`1` si `Statut_Remboursement == 'En souffrance (> 90 j)'`, sinon `0`) pour le suivi du *Portfolio at Risk > 90 jours*.
   - **`Tranche_Age`** : segmentation en `'Jeune (< 35 ans)'`, `'Adulte (35-50 ans)'` et `'Senior (> 50 ans)'`.

4. **Synthèse & export :**
   - Affiche le **Montant Total Accordé**, le **Montant Total Recouvré**, le **Taux de Recouvrement Global** et le **Portefeuille à Risque (PAR 90)**.
   - Exporte les données nettoyées vers `outputs/` (encodage `utf-8`, sans index).

---

## 📁 Structure du dépôt


```text
finance-etl-analytics/
├── data/
│   └── microfinance_donnees_brutes.csv   # Données brutes d'entrée                          
├── outputs/
│   └── microfinance_donnees_propre.csv  # Données nettoyées et enrichies
├── src/
│   └── script_nettoyage.py              # Script principal du pipeline ETL
└── README.md

## Installation
# Installer les dépendances nécessaires
pip install pandas numpy

# Depuis la racine de finance-etl-analytics, lancer le script :
python src/script_nettoyage.py