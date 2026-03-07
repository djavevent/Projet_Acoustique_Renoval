import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from PIL import Image, ImageOps
import os

# 1. Base de données complète des panneaux
panneaux_infos = {
    "Panneau 1": {"modele": "ISOMAT 2 CONFORT", "epaisseur": "32 mm", "masse":"4,14 kg/m²", "composition": "Alu / XPS / EPDM / Alu", "image": "P1.png", "col_index": 0, "color": "#1f77b4"},
    "Panneau 2": {"modele": "Faux plafond", "epaisseur": "51 mm", "masse":"4,08 kg/m²", "composition": "Alu / XPS / Alu", "image": "P2.png", "col_index": 1, "color": "#ff7f0e"},
    "Panneau 3": {"modele": "ISOMAT 2 PREMIUM", "epaisseur": "57 mm", "masse":"5,06 kg/m²","composition": "Alu / XPS / EPDM / Alu", "image": "P3.png", "col_index": 2, "color": "#2ca02c"},
    "Panneau 4": {"modele": "ISOMAT 2 PRESTIGE", "epaisseur": "70 mm", "masse":"5,42 kg/m²", "composition": "Alu / XPS / EPDM / Alu", "image": "P4.png", "col_index": 3, "color": "#d62728"},
    "Panneau 5": {"modele": "ISOMAT 2 PRESTIGE OPTIMA", "epaisseur": "70 mm", "masse":"5,25 kg/m²", "composition": "Alu / XPS / EPDM / Alu / Membrane absorbante", "image": "P5.png", "col_index": 4, "color": "#9467bd"},
    "Panneau 6": {"modele": "HOME ISO", "epaisseur": "97 mm", "masse":"8,14 kg/m²", "composition": "Alu / XPS Expansé / XPS Extrudé / EPDM / Alu / Membrane absorbante", "image": "P6.png", "col_index": 5, "color": "#8c564b"}
}

st.set_page_config(layout="wide", page_title="ENSIM x Rénoval") 
st.title("Comparateur Acoustique - Projet 4A ENSIM Rénoval")

# --- FONCTIONS DE CALCUL ---
def calculate_rw(freqs, tl_values):
    third_oct_freqs = [100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150]
    ref_curve_base = [-19, -16, -13, -10, -7, -4, -1, 0, 1, 2, 3, 4, 4, 4, 4, 4]
    tl_13 = []
    for f in third_oct_freqs:
        f_low, f_high = f / (2**(1/6)), f * (2**(1/6))
        mask = (freqs >= f_low) & (freqs <= f_high)
        tl_13.append(tl_values[mask].mean() if mask.any() else 0)
    tl_13 = np.array(tl_13)
    for rw_test in range(70, 0, -1):
        current_ref = np.array(ref_curve_base) + rw_test
        deficiencies = np.maximum(current_ref - tl_13, 0)
        if np.sum(deficiencies) <= 32.0:
            return rw_test, third_oct_freqs, current_ref
    return 0, third_oct_freqs, np.zeros(16)

def to_third_octave(freqs, values):
    third_oct_freqs = [100, 125, 160, 200, 250, 315, 400, 500, 630, 800, 1000, 1250, 1600, 2000, 2500, 3150, 4000, 5000]
    res_v = []
    for f in third_oct_freqs:
        f_low, f_high = f / (2**(1/6)), f * (2**(1/6))
        mask = (freqs >= f_low) & (freqs <= f_high)
        res_v.append(values[mask].mean() if mask.any() else None)
    return third_oct_freqs, res_v

# --- CHARGEMENT DES DONNÉES ---
@st.cache_data
def load_data():
    try:
        f_tl = pd.read_csv("freqs.txt", sep='\t', header=None, usecols=[0], names=['Frequency'])
        d_tl = pd.read_csv("Moyenne_TL.txt", sep='\t', header=None)
        df_tl = pd.concat([f_tl.reset_index(drop=True), d_tl.reset_index(drop=True)], axis=1)
        f_im = pd.read_csv("frequence.csv", header=None, names=['Frequency'])
        d_im = pd.read_csv("moyenne_6_panneaux.csv", header=None)
        df_im = pd.concat([f_im.reset_index(drop=True), d_im.reset_index(drop=True)], axis=1)
        return df_tl, df_im
    except Exception as e:
        st.error(f"Erreur fichiers : {e}")
        return None, None

df_tl, df_im = load_data()

# 2. Barre latérale

    
st.sidebar.header("Paramètres")
selection_par_defaut = ["Panneau 1", "Panneau 3", "Panneau 4", "Panneau 5", "Panneau 6"]
selection = st.sidebar.multiselect("Choisissez les panneaux :", options=list(panneaux_infos.keys()), default=selection_par_defaut)

mode_graph = st.sidebar.radio("Affichage Bruit Aérien :", ["Bande fine (Narrow Band)", "Tiers d'octave (1/3 Octave)"])
lissage = st.sidebar.slider("Lissage (Hz) - Narrow Band uniquement", 1, 200, 50)

st.sidebar.subheader("Options")
show_gauge = st.sidebar.toggle("Afficher la courbe de référence (Rw)", value=False)
show_v_grid = st.sidebar.toggle("Afficher les lignes verticales", value=True)

# 3. Fiches techniques
if selection:
    st.subheader("Fiches Techniques des panneaux (84mm x 94mm)")
    cols = st.columns(len(selection))
    rw_data = {}

    for i, p_name in enumerate(selection):
        info = panneaux_infos[p_name]
        with cols[i]:
            if df_tl is not None:
                rw_val, f_13, g_line = calculate_rw(df_tl['Frequency'], df_tl.iloc[:, info['col_index'] + 1])
                rw_data[p_name] = (f_13, g_line)
                st.metric(label=f"Indice $R_w$", value=f"{rw_val} dB")
            if os.path.exists(info['image']):
                st.image(Image.open(info['image']), width=250)
            
            st.markdown(f"""
            <span style="color:{info['color']}; font-size: 20px;">●</span> **{info['modele']}**
            * **Épaisseur :** {info['epaisseur']}
            * **Masse surfacique :** {info['masse']}
            * **Composition :** {info['composition']}
            ---
            """, unsafe_allow_html=True)

    # 4. GRAPHIQUE 1 : TRANSMISSION LOSS
    st.divider()
    st.subheader("1. Analyse de l'Affaiblissement Acoustique (Bruit Aérien)")
    
    if df_tl is not None:
        fig_tl = go.Figure()
        for p_name in selection:
            info = panneaux_infos[p_name]
            raw_y = df_tl.iloc[:, info['col_index'] + 1]
            
            if mode_graph == "Tiers d'octave (1/3 Octave)":
                f_x, v_y = to_third_octave(df_tl['Frequency'], raw_y)
                fig_tl.add_trace(go.Scatter(x=f_x, y=v_y, name=info['modele'], mode='lines+markers', line=dict(width=3, color=info['color'])))
            else:
                y_smooth = raw_y.rolling(window=lissage, center=True).mean()
                fig_tl.add_trace(go.Scatter(x=df_tl['Frequency'], y=y_smooth, name=info['modele'], line=dict(width=2.5, color=info['color'])))

            if show_gauge and p_name in rw_data:
                f_ref, g_ref = rw_data[p_name]
                fig_tl.add_trace(go.Scatter(x=f_ref, y=g_ref, name=f"Réf. ISO {info['modele']}", line=dict(width=2, dash='dot', color=info['color']), mode='lines+markers'))

        fig_tl.update_xaxes(type="log", title="Fréquence (Hz)", showgrid=show_v_grid, tickformat=".0f")
        fig_tl.update_yaxes(title="Indice d'affaiblissement TL (dB)")
        fig_tl.update_layout(height=500, template="plotly_white", hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_tl, use_container_width=True)
        st.info("💡 Pour le bruit aérien (TL), plus la courbe est haute, meilleure est l'isolation phonique du panneau.")

    # 5. GRAPHIQUE 2 : BRUIT D'IMPACT
    st.divider()
    st.subheader("2. Analyse du Niveau de Choc (Marteau d'Impact)")
    
    if df_im is not None:
        fig_im = go.Figure()
        for p_name in selection:
            info = panneaux_infos[p_name]
            fig_im.add_trace(go.Scatter(x=df_im['Frequency'], y=df_im.iloc[:, info['col_index'] + 1], name=info['modele'], line=dict(width=3, color=info['color']), mode='lines+markers'))

        fig_im.update_xaxes(type="log", title="Fréquence (Hz)", showgrid=show_v_grid, tickformat=".0f")
        fig_im.update_yaxes(title="Efficacité de réduction de choc [20 log(Pa/N)]")
        fig_im.update_layout(height=500, template="plotly_white", hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_im, use_container_width=True)
        st.info("💡 Pour le bruit d'impact, plus la courbe est basse, plus le panneau amortit efficacement les chocs (gouttes d'eau).")
else:
    st.info("👈 Sélectionnez des panneaux dans la barre latérale.")