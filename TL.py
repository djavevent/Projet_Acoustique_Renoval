import pandas as pd
import matplotlib.pyplot as plt

# 1. Chargement des fichiers
freq_file = "freqs.txt"
data_file = "Moyenne_TL.txt"

# Lecture des fréquences : 
# On force la lecture de la SEULE première colonne pour éviter les colonnes fantômes
freqs = pd.read_csv(freq_file, sep='\t', header=None, usecols=[0], names=['Frequency'])

# Lecture des données TL (les 6 colonnes)
data_tl = pd.read_csv(data_file, sep='\t', header=None)

# Pour éviter l'erreur de "Union", on s'assure que les deux objets sont des DataFrames simples
# et on les aligne par l'index de ligne
df = pd.concat([freqs.reset_index(drop=True), data_tl.reset_index(drop=True)], axis=1)

# Renommer les colonnes : 1 pour la fréquence + 6 pour les panneaux
panneaux_labels = ["Panneau 1", "Panneau 2", "Panneau 3", "Panneau 4", "Panneau 5", "Panneau 6"]
df.columns = ['Frequency'] + panneaux_labels

# 2. Configuration du graphique
plt.figure(figsize=(14, 8))
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

# 3. Traitement et tracé
for i, label in enumerate(panneaux_labels):
    # Calcul du moyennage glissant (50 Hz)
    # On ignore les valeurs NaN créées sur les bords par le rolling
    tl_smooth = df[label].rolling(window=50, center=True).mean()
    
    # Tracé : Courbe brute (alpha=0.15 pour la transparence)
    plt.plot(df['Frequency'], df[label], color=colors[i], alpha=0.15, linewidth=0.5)
    
    # Tracé : Courbe lissée
    plt.plot(df['Frequency'], tl_smooth, color=colors[i], label=f"{label} (Moy. 50Hz)", linewidth=2)

# 4. Mise en forme
plt.xscale('log')
plt.xlim(100, 5000)
plt.ylim(0, 60)

plt.title("Indice d'Affaiblissement Acoustique (TL) - Comparaison des 6 panneaux", fontsize=14)
plt.xlabel("Fréquence (Hz)", fontsize=12)
plt.ylabel("Transmission Loss (dB)", fontsize=12)

plt.grid(True, which='both', linestyle='--', alpha=0.5)
plt.legend(loc='upper left', fontsize=10, ncol=2) # Légende sur 2 colonnes pour la lisibilité

plt.tight_layout()
plt.show()