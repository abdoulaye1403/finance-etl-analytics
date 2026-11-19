import pandas as pd
import numpy as np
import os


def automatisation_pipeline_data(chemin_fichier_brut):
    """
    Pipeline ETL : Nettoyage, structuration et enrichissement
    des données .
    """
    print(f"🔄 Démarrage du traitement automatisé pour : {chemin_fichier_brut}...")
    
    if not os.path.exists(chemin_fichier_brut):
        print(f"❌ Erreur : Le fichier {chemin_fichier_brut} est introuvable.")
        return
    
    # 1. Chargement des données brutes
    df = pd.read_csv(chemin_fichier_brut)
    print(f"📊 Données chargées : {df.shape[0]} lignes, {df.shape[1]} colonnes.")

    # 2. Traitement des valeurs manquantes (Imputation propre)
    # - Secteur : Remplacer NaN par 'Non renseigné'
    df['Secteur_Activite'] = df['Secteur_Activite'].fillna('Non renseigné')

    # - Région : Remplacer NaN par 'Inconnue'
    df['Region'] = df['Region'].fillna('Inconnue')

    # - Âge : Imputer par la médiane de la population
    mediane_age = df['Age'].median()
    df['Age'] = df['Age'].fillna(mediane_age).astype(int)

    # 3. Enrichissement des Données (Feature Engineering)

    # A. Calcul du Taux de Remboursement (%)
    df['Taux_Remboursement_%'] = ((df['Montant_Rembourse_XOF'] / df['Montant_Pret_XOF']) * 100).round(1)

    # B. Calcul du Reste à Rembourser (Encours)
    df['Reste_A_Rembourser_XOF'] = df['Montant_Pret_XOF'] - df['Montant_Rembourse_XOF']

    # C. Indicateur PAR 90 (Portfolio at Risk > 90 jours - Prêts en souffrance)
    # En finance micro-crédit, 1 = Créance à haut risque, 0 = Sains/Risque faible
    df['Indicateur_PAR90'] = np.where(df['Statut_Remboursement'] == 'En souffrance (> 90 j)', 1, 0)

    # D. Segmentation par Tranche d'Âge (Focus Jeunesse)
    def categoriser_age(age):
        if age < 35:
            return 'Jeune (< 35 ans)'
        elif age <= 50:
            return 'Adulte (35-50 ans)'
        else:
            return 'Senior (> 50 ans)'

    df['Tranche_Age'] = df['Age'].apply(categoriser_age)

    # 5. Nettoyage des doublons stricts
    df = df.drop_duplicates()

    # 6. Résumé statistique rapide des résultats
    print("\n--- 📈 RÉSUMÉ DU PORTEFEUILLE NETTOYÉ ---")
    print(f"• Montant Total Accordé : {df['Montant_Pret_XOF'].sum():,.0f} XOF")
    print(f"• Montant Total Recouvré : {df['Montant_Rembourse_XOF'].sum():,.0f} XOF")
    print(f"• Taux de Recouvrement Global : {(df['Montant_Rembourse_XOF'].sum() / df['Montant_Pret_XOF'].sum() * 100):.1f} %")
    print(f"• Portefeuille à Risque (PAR 90) : {df['Indicateur_PAR90'].sum()} prêts en souffrance ({(df['Indicateur_PAR90'].mean() * 100):.1f} % du portefeuille)")
    
    # 7. Export du fichier propre
    df.to_csv('microfinance_donnees_propre.csv', index=False,encoding='utf-8')
    print(f"✅ Fichier nettoyé généré avec succès : {'microfinance_donnees_propre.csv'}")
    return df

# Exécution du pipeline
FICHIER_ENTREE = "data/microfinance_donnees_brutes.csv"
df_clean = automatisation_pipeline_data(FICHIER_ENTREE)