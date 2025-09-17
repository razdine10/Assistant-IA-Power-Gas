"""
Home page for the Power & Gas Assistant.

This Streamlit app offers two main features:
- A chatbot for electricity and gas related questions
- An automatic email reply generator
"""
import streamlit as st


# Global app configuration
st.set_page_config(
    page_title="Assistant Power & Gas",
    page_icon="🔌",
    layout="wide",
)

# Custom CSS styles for the UI
st.markdown(
    """
    <style>
    .block-container {padding-top: 1.5rem;}
    .hero {
        background: linear-gradient(135deg, #E6E6FA, #B0E0E6);
        border: 1px solid #e5e7eb;
        padding: 36px 32px;
        border-radius: 20px;
        margin-bottom: 6px;
    }
    .hero h1 {
        margin: 0 0 8px; 
        font-size: 52px; 
        line-height: 1.05;
    }
    .hero p {
        margin: 0; 
        color: #1C1C3C; 
        font-size: 18px; 
        opacity: .85;
    }
    .badge {
        display: inline-flex; 
        gap: 8px; 
        align-items: center; 
        padding: 6px 10px; 
        border-radius: 999px; 
        background: #ede9fe; 
        color: #6A5ACD; 
        border: 1px solid #ddd6fe; 
        font-weight: 600; 
        font-size: 13px; 
        margin-bottom: 10px;
    }
    .feature {
        background: #fff; 
        border: 1px solid #eef1f5; 
        border-radius: 12px; 
        padding: 16px;
    }
    .feature h4 {margin: 0 0 6px;}
    .small {color: #6b7280; font-size: 13px;}
    /* Boutons CTA sur la page d'accueil uniquement */
    div.stButton > button { 
        height: 64px; 
        font-size: 18px; 
        border-radius: 12px; 
        font-weight: 700; 
        border: 1px solid #c7d2fe; 
        background: linear-gradient(180deg, #ede9fe, #e0e7ff);
        color: #1C1C3C;
    }
    div.stButton > button:hover { 
        filter: brightness(0.98); 
        border-color: #6A5ACD;
    }
    .card {
        background: #fff; 
        border: 1px solid #e5e7eb; 
        border-radius: 14px; 
        padding: 18px;
    }
    .stat {
        background: #ffffff; 
        border: 1px dashed #e5e7eb; 
        border-radius: 12px; 
        padding: 14px; 
        text-align: center;
    }
    .kicker {
        color: #6A5ACD; 
        font-weight: 700; 
        letter-spacing: .02em;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Hero section with title and description
st.markdown(
    """
    <div class="hero">
      <div class="badge">🔌 Assistant IA énergie</div>
      <h1>Assistant Power & Gas</h1>
      <p>Répondez aux questions électricité & gaz et rédigez des e‑mails 
      impeccables.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# Primary action buttons
st.subheader("Commencer")
colonne_chatbot, colonne_emails = st.columns([1, 1])

with colonne_chatbot:
    if st.button("🤖 Ouvrir le Chatbot", use_container_width=True):
        st.switch_page("pages/01_Chatbot.py")
    st.caption(
        "Questions sur tarifs, index, puissance, taxes, zones GRDF…"
    )

with colonne_emails:
    if st.button("✉️ Générer des réponses e‑mail", use_container_width=True):
        st.switch_page("pages/02_Emails.py")
    st.caption(
        "Rédigez des réponses claires et professionnelles "
        "en quelques secondes."
    )

# Visual divider
st.divider()

# Important notes and limitations
st.markdown(
    """
    - Les réponses IA peuvent contenir des approximations. 
      Vérifiez les informations sensibles.
    - Pour des données tarifaires à jour, consultez la CRE, Enedis, 
      GRDF et les fournisseurs.
    """
)

# Links to official resources
st.markdown(
    """
    **Ressources officielles :** 
    [CRE](https://www.cre.fr/) · 
    [Enedis](https://www.enedis.fr/) · 
    [GRDF](https://www.grdf.fr/) · 
    [Service‑public](https://www.service-public.fr/) · 
    [EDF](https://www.edf.fr/) · 
    [ENGIE](https://particuliers.engie.fr/)
    """
)