import pandas as pd
import matplotlib.pyplot as plt

# 1. Chargement des fichiers
# frequence.csv : 21 valeurs (tiers d'octave de 100Hz à 10kHz)
# moyenne_6_panneaux.csv : 6 colonnes de données en dB
freq_file = "frequence.csv"
data_file = "moyenne_6_panneaux.csv"

try:
    # Lecture des fréquences (colonne unique)
    freqs = pd.read_csv(freq_file, header=None)[0]

    # Lecture des données d'impact (6 colonnes)
    data_impact = pd.read_csv(data_file, header=None)

    # Noms des panneaux pour la légende
    panneaux_labels = [
        "Panneau 1 (ISOMAT 2 CONFORT)", 
        "Panneau 2 (Faux plafond)", 
        "Panneau 3 (ISOMAT 2 PREMIUM)", 
        "Panneau 4 (ISOMAT 2 PRESTIGE)", 
        "Panneau 5 (PRESTIGE OPTIMA)", 
        "Panneau 6 (HOME ISO)"
    ]

    # 2. Configuration du graphique
    plt.figure(figsize=(12, 7))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

    # 3. Tracé des courbes
    # Note : Pas de lissage glissant ici car ce sont des tiers d'octave (21 points seulement)
    for i in range(6):
        plt.plot(
            freqs, 
            data_impact[i], 
            marker='o', 
            markersize=4, 
            color=colors[i], 
            label=panneaux_labels[i], 
            linewidth=2
        )

    # 4. Mise en forme Logarithmique
    plt.xscale('log')
    
    # Définition des étiquettes de l'axe X pour les tiers d'octave
    ticks = [100, 200, 500, 1000, 2000, 5000, 10000]
    plt.xticks(ticks, [str(t) for t in ticks])
    
    plt.xlim(100, 10000)
    plt.ylim(0, 100) # Échelle adaptée au bruit d'impact (souvent plus élevé que le TL)

    # Titres et légendes
    plt.title("Niveau de Pression Acoustique de Choc (Test au Marteau d'Impact)", fontsize=14)
    plt.xlabel("Fréquence (Hz)", fontsize=12)
    plt.ylabel("Niveau de pression transmis (dB)", fontsize=12)

    plt.grid(True, which='both', linestyle='--', alpha=0.6)
    plt.legend(loc='upper right', fontsize=9)

    plt.tight_layout()
    
    # Enregistrement du résultat
    plt.savefig("Analyse_Impact_6Panneaux.png", dpi=300)
    print("Graphique généré avec succès : Analyse_Impact_6Panneaux.png")
    plt.show()

except Exception as e:
    print(f"Erreur lors de l'exécution : {e}")