import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from PIL import Image, ImageOps
import os

# 1. Base de données complète des panneaux (ENSIM / Rénoval)
panneaux_infos = {
    "Panneau 1": {"modele": "ISOMAT 2 CONFORT", "epaisseur": "32mm", "composition": "Alu / XPS / EPDM / Alu", "image": "P1.png", "col_index": 0},
    "Panneau 2": {"modele": "Faux plafond", "epaisseur": "51mm", "composition": "Alu / XPS / Alu", "image": "P2.png", "col_index": 1},
    "Panneau 3": {"modele": "ISOMAT 2 PREMIUM", "epaisseur": "57mm", "composition": "Alu / XPS / EPDM / Alu", "image": "P3.png", "col_index": 2},
    "Panneau 4": {"modele": "ISOMAT 2 PRESTIGE", "epaisseur": "70mm", "composition": "Alu / XPS / EPDM / Alu", "image": "P4.png", "col_index": 3},
    "Panneau 5": {"modele": "ISOMAT 2 PRESTIGE OPTIMA", "epaisseur": "70mm", "composition": "Alu / XPS / EPDM / Alu / Membrane cuir", "image": "P5.png", "col_index": 4},
    "Panneau 6": {"modele": "HOME ISO", "epaisseur": "97mm", "composition": "Alu / XPS Expansé / XPS Extrudé / EPDM / Alu", "image": "P6.png", "col_index": 5}
}

st.set_page_config(layout="wide", page_title="ENSIM x Rénoval") 
st.title("Comparateur Acoustique Interactif - Projet 4A ENSIM Rénoval")

# --- FONCTION DE CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_acoustic_data():
    try:
        # Lecture des fréquences (1ère colonne)
        freqs = pd.read_csv("freqs.txt", sep='\t', header=None, usecols=[0], names=['Frequency'])
        # Lecture des 6 colonnes de données (Moyenne_TL.txt)
        data_tl = pd.read_csv("Moyenne_TL.txt", sep='\t', header=None)
        # Fusion
        full_df = pd.concat([freqs.reset_index(drop=True), data_tl.reset_index(drop=True)], axis=1)
        return full_df
    except Exception as e:
        st.error(f"Erreur de chargement des fichiers : {e}")
        return None

df_global = load_acoustic_data()

# 2. Barre latérale
st.sidebar.header("Paramètres")
selection = st.sidebar.multiselect(
    "Choisissez les panneaux à comparer :", 
    options=list(panneaux_infos.keys()),
    default=["Panneau 2", "Panneau 5"]
)

lissage = st.sidebar.slider("Niveau de lissage (Fenêtre en Hz)", 1, 200, 50)

# 3. Affichage des fiches techniques et indicateurs
if selection:
    st.subheader("Performance Globale & Fiches Techniques")
    
    cols = st.columns(len(selection))
    
    for i, p_name in enumerate(selection):
        info = panneaux_infos[p_name]
        with cols[i]:
            # Calcul de la valeur moyenne de TL (dB)
            if df_global is not None:
                col_idx = info['col_index']
                mean_tl = df_global.iloc[:, col_idx + 1].mean()
                st.metric(label=f"Réduction Moyenne", value=f"{mean_tl:.1f} dB")
            
            # Gestion de l'image (Taille réduite à 250px comme demandé)
            if os.path.exists(info['image']):
                img = Image.open(info['image'])
                img = ImageOps.exif_transpose(img)
                st.image(img, width=250) 
            else:
                st.info(f"📸 Image {info['image']} manquante")
            
            # MINI FICHE TECHNIQUE
            st.markdown(f"""
            **{p_name}**
            * **Modèle :** {info['modele']}
            * **Épaisseur :** {info['epaisseur']}
            * **Composition :** {info['composition']}
            ---
            """, unsafe_allow_html=True)
    

    # 4. Graphique Comparatif Plotly
    st.divider()
    if df_global is not None:
        fig = go.Figure()

        for p_name in selection:
            col_idx = panneaux_infos[p_name]['col_index']
            y_values = df_global.iloc[:, col_idx + 1] 
            y_smooth = y_values.rolling(window=lissage, center=True).mean()

            fig.add_trace(go.Scatter(
                x=df_global['Frequency'], 
                y=y_smooth, 
                name=f"{p_name} ({panneaux_infos[p_name]['modele']})",
                mode='lines',
                line=dict(width=2.5)
            ))

        fig.update_xaxes(
            type="log", title="Fréquence (Hz)", 
            gridcolor='rgba(200,200,200,0.3)', tickformat=".0f",
            range=[np.log10(100), np.log10(5000)]
        )
        fig.update_yaxes(
            title="Indice d'affaiblissement TL (dB)", 
            gridcolor='rgba(200,200,200,0.3)',
            range=[0, 60]
        )
        fig.update_layout(
            height=600,
            template="plotly_white",
            margin=dict(l=20, r=20, t=40, b=20),
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👈 Sélectionnez des panneaux dans la barre latérale pour afficher la comparaison.")