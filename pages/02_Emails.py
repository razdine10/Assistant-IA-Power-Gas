"""
Email reply generator page.

This page creates professional email replies based on the incoming email
and the selected tone/language.
"""
import streamlit as st

from ai_utils import generer_reponse_email


st.set_page_config(
    page_title="Réponses E-mails IA", 
    page_icon="✉️"
)

st.title("📧 Génération de réponses e-mail")
st.caption(
    "Rédigez automatiquement des réponses claires et professionnelles"
)

with st.expander("ℹ️ Guide des paramètres IA"):
    st.markdown("""
    ### 🤖 Choix du modèle IA
    
    **llama-3.1-8b-instant** (par défaut)
    - Plus rapide et moins coûteux
    - Bonnes réponses pour la plupart des e-mails
    - Idéal pour un usage quotidien
    - Excellent pour les réponses professionnelles
    
    **gemma2-9b-it**
    - Modèle alternatif de Google
    - Bon pour les réponses créatives
    - Style d'écriture différent
    - Utile pour varier les formulations
    
    **llama-3.3-70b-versatile**
    - Plus puissant et précis
    - Meilleur pour les e-mails complexes/délicats
    - Plus lent et plus coûteux
    
    💡 **Conseil :** Commencez avec llama-3.1-8b-instant, 
    passez au 70b si vous avez besoin de plus de finesse et essayez
    gemma2-9b-it pour des styles de rédaction différents.
    
    ### 🎚️ Slider Créativité (Temperature)
    
    **Temperature basse (0.0 - 0.3)** ← Votre réglage actuel
    - Réponses plus **prévisibles** et **cohérentes**
    - L'IA choisit les mots les plus probables
    - Parfait pour des réponses professionnelles factuelles
    
    **Temperature élevée (0.7 - 1.0)**
    - Réponses plus **créatives** et **variées**
    - L'IA prend plus de "risques" dans le choix des mots
    - Plus de chance d'avoir des formulations originales
    
    💡 **Pour vos e-mails :** Gardez 0.2-0.3 pour la précision, 
    montez à 0.4-0.5 si vous voulez plus de variété dans les formulations.
    """)

# Visual separator
st.markdown("---")

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
    
    # Creativity (temperature) slider
    temperature = st.slider(
        "Créativité (temperature)", 
        0.0, 
        1.0, 
        0.3, 
        0.05
    )

# Two columns: subject and language
colonne_objet, colonne_langue = st.columns([2, 1])
with colonne_objet:
    objet_email = st.text_input("Objet (optionnel)")
with colonne_langue:
    langue_reponse = st.selectbox("Langue", ["fr", "en"], index=0)

# Text area for the incoming email
texte_email_recu = st.text_area(
    "E-mail reçu",
    height=220,
    placeholder=(
        "Collez ici l'e-mail auquel répondre (plain text).\n"
        "Ex: réclamation facture, demande d'informations, "
        "relance commerciale, etc."
    ),
)

# Tone selection
ton_reponse = st.radio(
    "Ton",
    options=["professionnel", "empathique", "ferme", "convivial"],
    horizontal=True,
)

# Additional constraints (optional)
contraintes_supplementaires = st.text_input(
    "Contraintes supplémentaires (optionnel)",
    placeholder=(
        "Ex: inclure références client, demander un justificatif, "
        "fixer un délai…"
    ),
)

# Generate button
generer_reponse = st.button("Générer la réponse")

# Handle generation
if generer_reponse and texte_email_recu.strip():
    # Compose the input text, prepend subject when provided
    if objet_email:
        texte_source = f"Objet: {objet_email}\n\n{texte_email_recu}"
    else:
        texte_source = texte_email_recu
    
    # Generate the reply with a spinner
    with st.spinner("Rédaction de l'e-mail…"):
        reponse_generee = generer_reponse_email(
            texte_email=texte_source,
            ton=ton_reponse,
            langue=langue_reponse,
            instructions_supplementaires=contraintes_supplementaires,
            modele=modele_choisi,
            temperature=temperature,
            tokens_max=700,
        )

    # Display the reply with a styled box
    st.subheader("Réponse proposée")
    st.markdown(
        """
        <style>
        .reply-box {
            background: #f8f9fb;
            padding: 16px 18px;
            border-radius: 12px;
            border: none;
            box-shadow: 0 1px 2px rgba(0,0,0,0.06);
            white-space: pre-wrap;
            line-height: 1.55;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<div class='reply-box'>{reponse_generee}</div>", 
        unsafe_allow_html=True
    )
    
    # Download button
    st.download_button(
        label="Télécharger .txt",
        data=reponse_generee,
        file_name="reponse_email.txt",
        mime="text/plain",
    )

# Final tip
st.divider()
st.markdown(
    """
    **Conseil :** ajoutez des éléments factuels (références, dates, montants) 
    pour une réponse plus précise.
    """
)


