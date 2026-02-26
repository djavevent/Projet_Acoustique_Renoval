import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

# 1. Recherche automatique des 6 fichiers NarrowBands
file_list = sorted(glob.glob("*_NarrowBands.txt"))

plt.figure(figsize=(14, 8))

# Palette de couleurs distinctes
colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b']

for i, file in enumerate(file_list):
    # Nom du panneau pour la légende
    label_name = os.path.basename(file).split('_TL')[0]
    
    # Lecture des données (tabulation)
    data = pd.read_csv(file, sep='\t')
    
    # --- MOYENNAGE 50 Hz ---
    # Le pas étant de 1 Hz, une fenêtre de 50 points = 50 Hz
    data['TL_avg'] = data['TL (dB)'].rolling(window=50, center=True).mean()
    
    # Tracé : Bande fine en fond (très clair) + Courbe moyennée (gras)
    plt.plot(data['Frequency (Hz)'], data['TL (dB)'], color=colors[i], alpha=0.15, linewidth=0.5)
    plt.plot(data['Frequency (Hz)'], data['TL_avg'], color=colors[i], label=f"{label_name} (Moy. 50Hz)", linewidth=2)

# 2. Mise en forme Log/Ingénieur
plt.xscale('log')
plt.xlim(100, 5000)
plt.ylim(0, 60) # Ajuster selon vos maximums

# Graduation standard acoustique
ticks = [100, 200, 500, 1000, 2000, 5000]
plt.xticks(ticks, [str(t) for t in ticks])

plt.grid(True, which="both", ls="-", alpha=0.3)
plt.xlabel('Fréquence (Hz)', fontsize=12)
plt.ylabel('Transmission Loss (dB)', fontsize=12)
plt.title('Comparaison TL : Bandes Fines avec Moyennage Glissant 50 Hz', fontsize=14, fontweight='bold')

plt.legend(loc='upper left', bbox_to_anchor=(1, 1), fontsize=10)
plt.tight_layout()

# 3. Sauvegarde
plt.savefig('Comparaison_TL_Moyenne_50Hz.png', dpi=300)
plt.show()