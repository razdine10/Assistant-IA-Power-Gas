"""
Chatbot page for electricity and gas questions.

This page lets users ask energy-related questions and get AI answers using
Groq, keeping the chat history within the Streamlit session state.
"""
from typing import Dict, List

import streamlit as st

from ai_utils import generer_reponse_ia


# Page configuration
st.set_page_config(
    page_title="Chatbot Électricité & Gaz", 
    page_icon="⚡️"
)

# Title and short description
st.title("🤖 Chatbot Électricité & Gaz")
st.caption(
    "Questions sur tarifs, index, puissance, taxes, "
    "évolutions de prix, etc."
)

# Collapsible help: model and creativity guidance
with st.expander("ℹ️ Guide des paramètres IA"):
    st.markdown("""
    ### 🤖 Choix du modèle IA
    
    **llama-3.1-8b-instant** (par défaut)
    - Plus rapide et moins coûteux
    - Bonnes réponses pour la plupart des questions
    - Idéal pour un usage quotidien
    - Excellent pour les questions sur l'énergie
    
    **gemma2-9b-it**
    - Modèle alternatif de Google
    - Bon pour des réponses créatives
    - Peut donner des perspectives différentes
    - Utile pour varier les explications
    
    **llama-3.3-70b-versatile**
    - Plus puissant et précis
    - Meilleur pour des questions complexes et analyses détaillées
    - Plus lent et plus coûteux
    
    💡 **Conseil :** Commencez avec 8b-instant. Passez au 70b si vous avez
    besoin de plus de profondeur/rigueur. Essayez gemma2 pour varier le style.
    
    ### 🎚️ Slider Créativité (Temperature)
    
    **Temperature basse (0.0 - 0.3)** ← recommandé pour des réponses fiables
    - Réponses plus **prévisibles** et **cohérentes**
    - L'IA choisit les mots les plus probables
    - Parfait pour des réponses techniques factuelles
    
    **Temperature élevée (0.7 - 1.0)**
    - Réponses plus **créatives** et **variées**
    - L'IA prend plus de "risques" dans le choix des mots
    - Plus de chance d'avoir des explications originales
    
    💡 **Astuce :** Pour des questions énergie, gardez 0.2–0.3 pour la
    précision; montez à 0.4–0.5 si vous voulez plus de créativité.
    """)

# Sidebar with model/temperature controls
with st.sidebar:
    st.subheader("Paramètres IA")
    
    # Model selection
    modele_choisi = st.selectbox(
        "Modèle",
        options=[
            "llama-3.1-8b-instant",
            "gemma2-9b-it",
            "llama-3.3-70b-versatile",
        ],
        index=0,
    )

    # Creativity (temperature)
    temperature = st.slider(
        "Créativité (temperature)", 
        0.0, 
        1.0, 
        0.2, 
        0.05
    )
    
    # Official sources mode (disabled for now)
    mode_sources = False
    
    # Button to clear history
    effacer_historique = st.button("Effacer l'historique")

# Conversation history initialization
cle_historique = "energy_chat_history"
if cle_historique not in st.session_state or effacer_historique:
    st.session_state[cle_historique] = []

# Base system instructions for the assistant
prompt_systeme_base = (
    "Tu es un assistant expert en électricité et gaz en France. "
    "Réponds en français, de manière rigoureuse et actionnable. "
    "Couvre notamment : tarifs réglementés et offres de marché, "
    "taxes et contributions (CSPE, CTA, TURPE), puissance souscrite (kVA), "
    "kWh, heures pleines/creuses, index Linky; "
    "pour le gaz : conversion m³→kWh (coefficient, PCS/PCI), "
    "zones GRDF, régularisations de facture. "
    "Si la question est ambiguë, demande des précisions avant de conclure. "
    "Fournis des étapes claires (1,2,3). "
    "Pour toute donnée tarifaire susceptible d'évoluer, "
    "indique la méthode de calcul. Ne donne pas de conseils financiers."
)

# Append source citation instructions if enabled
prompt_systeme_final = prompt_systeme_base
if mode_sources:
    prompt_systeme_final += (
        " Cite explicitement au moins une source officielle pertinente "
        "avec un lien court: CRE, Enedis, GRDF, EDF, ENGIE, service‑public."
    )

# Render prior messages
for message in st.session_state[cle_historique]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
question_utilisateur = st.chat_input(
    "Posez votre question (ex: Estimation facture, "
    "heures creuses, index Linky)…"
)

# Handle a new question
if question_utilisateur:
    # Add the user question to history
    st.session_state[cle_historique].append({
        "role": "user", 
        "content": question_utilisateur
    })

    # Generate and show the assistant answer
    with st.chat_message("assistant"):
        with st.spinner("Rédaction de la réponse…"):
            # Get the full history
            historique_complet = st.session_state[cle_historique]
            
            # Adjust temperature if sources mode is active
            if mode_sources:
                temperature_effective = min(temperature, 0.3)
            else:
                temperature_effective = temperature
            
            # Generate the AI response
            reponse = generer_reponse_ia(
                message_utilisateur=None,
                prompt_systeme=prompt_systeme_final,
                messages=historique_complet,
                modele=modele_choisi,
                temperature=temperature_effective,
                tokens_max=800,
                domaine_secours="energy",
            )
            
            # Render the answer
            st.markdown(reponse)
            
            # Append assistant answer to history
            st.session_state[cle_historique].append({
                "role": "assistant", 
                "content": reponse
            })

# Divider and a short tip
st.divider()
st.markdown(
    """
    **Astuce :** pour affiner une estimation, indiquez votre offre, 
    puissance (kVA), consommation annuelle (kWh) et zone.
    """
)


