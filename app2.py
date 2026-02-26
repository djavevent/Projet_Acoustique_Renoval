import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from PIL import Image, ImageOps

# 1. Base de données complète des panneaux (ENSIM / Rénoval)
panneaux_infos = {
    "Panneau 1": {"modele": "ISOMAT 2 CONFORT", "epaisseur": "32mm", "composition": "Alu / XPS / EPDM / Alu", "image": "P1.png"},
    "Panneau 2": {"modele": "ISOMAT 2 PREMIUM", "epaisseur": "51mm", "composition": "Alu / XPS / Alu", "image": "P2.png"},
    "Panneau 3": {"modele": "ISOMAT 2 CONFORT", "epaisseur": "57mm", "composition": "Alu / XPS / EPDM / Alu", "image": "P3.png"},
    "Panneau 4": {"modele": "ISOMAT 2 PRESTIGE", "epaisseur": "70mm", "composition": "Alu / XPS / EPDM / Alu", "image": "P4.png"},
    "Panneau 5": {"modele": "PRESTIGE OPTIMA", "epaisseur": "70mm", "composition": "Alu / XPS / EPDM / Alu / Membrane cuir", "image": "P5.png"},
    "Panneau 6": {"modele": "HOME ISO", "epaisseur": "97mm", "composition": "Alu / XPS Expansé / XPS Extrudé / EPDM / Alu", "image": "P6.png"}
}

st.set_page_config(layout="wide", page_title="ENSIM x Rénoval") 
st.title("Comparateur Acoustique Interactif - Projet 4A ENSIM Rénoval")

# 2. Barre latérale
st.sidebar.header("Paramètres")
selection = st.sidebar.multiselect(
    "Choisissez les panneaux à comparer :", 
    options=list(panneaux_infos.keys()),
    default=["Panneau 2", "Panneau 5"]
)

# 3. Affichage des fiches techniques
if selection:
    st.subheader("Fiches Techniques & Compositions")
    
    # Création des colonnes
    cols = st.columns(len(selection))
    
    for i, p_name in enumerate(selection):
        info = panneaux_infos[p_name]
        with cols[i]:
            # Traitement de l'image
            img = Image.open(info['image'])
            img = ImageOps.exif_transpose(img)
            
            # AFFICHAGE IMAGE (Taille réduite à 150px de large pour plus de clarté)
            st.image(img, width=250) 
            
            # MINI FICHE TECHNIQUE
            st.markdown(f"""
            **{p_name}**
            * **Modèle :** {info['modele']}
            * **Épaisseur :** {info['epaisseur']}
            * **Composition :** {info['composition']}
            ---
            """, unsafe_allow_html=True)

    # 4. Graphique Comparatif
    st.divider()
    fig = go.Figure()

    for p_name in selection:
        try:
            # On cherche le fichier correspondant
            df = pd.read_csv(f"{p_name}_NarrowBands.txt", sep='\t')
            
            # Moyennage glissant 50 Hz
            df['TL_smooth'] = df['TL (dB)'].rolling(window=50, center=True).mean()

            fig.add_trace(go.Scatter(
                x=df['Frequency (Hz)'], 
                y=df['TL_smooth'], 
                name=f"{p_name}",
                mode='lines',
                line=dict(width=2.5)
            ))
        except FileNotFoundError:
            st.error(f"⚠️ Fichier `{p_name}_NarrowBands.txt` introuvable.")

    fig.update_xaxes(type="log", title="Fréquence (Hz)", gridcolor='rgba(200,200,200,0.3)', tickformat=".0f")
    fig.update_yaxes(title="Indice d'affaiblissement TL (dB)", gridcolor='rgba(200,200,200,0.3)')
    fig.update_layout(
        height=550,
        margin=dict(l=20, r=20, t=40, b=20),
        hovermode="x unified",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )

    st.plotly_chart(fig, use_container_width=True)


else:
    st.info("👈 Sélectionnez des panneaux dans la barre latérale pour afficher les données.")