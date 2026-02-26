import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from PIL import Image, ImageOps # Ajoute cet import

# 1. Base de données complète des panneaux (ENSIM / Rénoval)
panneaux_infos = {
    "Panneau 1": {"modele": "ISOMAT 2 CONFORT", "epaisseur": "32mm", "composition": "Alu / XPS / EPDM / Alu", "image": "P1.png"},
    "Panneau 2": {"modele": "ISOMAT 2 PREMIUM", "epaisseur": "51mm", "composition": "Alu / XPS / Alu", "image": "P2.png"},
    "Panneau 3": {"modele": "ISOMAT 2 CONFORT", "epaisseur": "57mm", "composition": "Alu / XPS / EPDM / Alu", "image": "P3.png"},
    "Panneau 4": {"modele": "ISOMAT 2 PRESTIGE", "epaisseur": "70mm", "composition": "Alu / XPS / EPDM / Alu", "image": "P4.png"},
    "Panneau 5": {"modele": "PRESTIGE OPTIMA", "epaisseur": "70mm", "composition": "Alu / XPS / EPDM / Alu / Membrane cuir", "image": "P5.png"},
    "Panneau 6": {"modele": "HOME ISO", "epaisseur": "97mm", "composition": "Alu / XPS Expansé / XPS Extrudé / EPDM / Alu", "image": "P6.png"}
}

st.set_page_config(layout="wide") # Utilise toute la largeur de l'écran
st.title("🚀 Comparateur Acoustique Interactif - Projet Rénoval")

# 2. Barre latérale pour la sélection multiple
st.sidebar.header("Paramètres de comparaison")
selection = st.sidebar.multiselect(
    "Choisissez les panneaux à comparer :", 
    options=list(panneaux_infos.keys()),
    default=["Panneau 2", "Panneau 5"] # Comparaison intéressante par défaut
)

# 3. Affichage des fiches techniques en colonnes
if selection:
    st.subheader("🔍 Détails techniques des panneaux sélectionnés")
    cols = st.columns(len(selection))
    for i, p_name in enumerate(selection):
        info = panneaux_infos[p_name]
        with cols[i]:
            img = Image.open(info['image'])
            # Cette ligne corrige l'orientation automatiquement selon les données EXIF
            img = ImageOps.exif_transpose(img) 
    
            st.image(img, use_container_width=True)
            st.write(f"**{p_name}**")
            
    # 4. Graphique Comparatif
    st.divider()
    fig = go.Figure()

    for p_name in selection:
        # Note : assure-toi que tes fichiers sont nommés exactement comme les clés (ex: Panneau 1_NarrowBands.txt)
        try:
            df = pd.read_csv(f"{p_name}_NarrowBands.txt", sep='\t')
            # Moyennage glissant 50 Hz pour la lisibilité
            df['TL_smooth'] = df['TL (dB)'].rolling(window=50, center=True).mean()

            # Ajout de la courbe moyennée
            fig.add_trace(go.Scatter(
                x=df['Frequency (Hz)'], 
                y=df['TL_smooth'], 
                name=f"{p_name} (Lissé 50Hz)",
                mode='lines',
                line=dict(width=3)
            ))
        except FileNotFoundError:
            st.error(f"Fichier de données manquant pour le {p_name}")

    fig.update_xaxes(type="log", title="Fréquence (Hz)", gridcolor='lightgray')
    fig.update_yaxes(title="Indice d'affaiblissement TL (dB)", gridcolor='lightgray')
    fig.update_layout(
        height=600,
        title="Comparaison du Transmission Loss (Données NarrowBands lissées)",
        hovermode="x unified",
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )

    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Sélectionnez au moins un panneau dans la barre latérale pour commencer la comparaison.")