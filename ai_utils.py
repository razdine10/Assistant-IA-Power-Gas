"""
AI utilities.

This module centralizes helper functions to communicate with the Groq API
and to generate automated answers for the chatbot and the email page.
"""
import os
from typing import Dict, List, Optional

# Try to import Groq. If unavailable, set the symbol to None
try:
    from groq import Groq
except ImportError:
    Groq = None


# Default model and generation constants
MODELE_PAR_DEFAUT = "llama-3.1-8b-instant"
TEMPERATURE_CHATBOT = 0.2
TEMPERATURE_EMAIL = 0.3
TOKENS_MAX_CHATBOT = 1200
TOKENS_MAX_EMAIL = 900


def recuperer_cle_groq(cle_explicite: Optional[str]) -> Optional[str]:
    """
    Retrieve a Groq API key from multiple possible sources.

    Resolution order:
    1) The explicit function argument
    2) Environment variable GROQ_API_KEY
    3) Streamlit secrets

    Args:
        cle_explicite: API key provided directly to the function.

    Returns:
        The resolved API key or None if it cannot be found.
    """
    # First, check the explicit argument
    if cle_explicite and cle_explicite.strip():
        return cle_explicite.strip()

    # Then check environment variables
    cle_env = os.getenv("GROQ_API_KEY")
    if cle_env:
        return cle_env

    # Finally, try Streamlit secrets
    try:
        import streamlit as st
        
        cle_secrete = st.secrets.get("GROQ_API_KEY")
        if cle_secrete:
            return str(cle_secrete)
    except Exception:
        # If Streamlit is not available here, continue silently
        pass

    return None


def construire_messages(
    message_utilisateur: Optional[str],
    prompt_systeme: Optional[str],
    historique: Optional[List[Dict[str, str]]],
) -> List[Dict[str, str]]:
    """
    Build a Groq-compatible messages list.

    The order is: system prompt (if any), then conversation history, then the
    current user message.

    Args:
        message_utilisateur: Current user input.
        prompt_systeme: System instructions for the assistant.
        historique: Prior messages in the conversation.

    Returns:
        A list of message dicts for the chat completion API.
    """
    messages = []

    # Start with the system prompt if present
    if prompt_systeme:
        messages.append({"role": "system", "content": prompt_systeme})

    # Then append previous conversation messages
    if historique:
        for message in historique:
            role = message.get("role", "user")
            contenu = message.get("content", "")
            if contenu:  # Skip empty messages
                messages.append({"role": role, "content": contenu})

    # Finally append the current user message
    if message_utilisateur:
        messages.append({"role": "user", "content": message_utilisateur})

    return messages


def appeler_groq(
    messages: List[Dict[str, str]],
    modele: str,
    temperature: float,
    tokens_max: int,
    cle_api: Optional[str],
) -> str:
    """
    Call Groq chat completions API and return the generated answer.

    Args:
        messages: Message list to send to the API.
        modele: Model name to use.
        temperature: Creativity level (0.0–1.0).
        tokens_max: Maximum number of tokens to generate.
        cle_api: Groq API key.

    Returns:
        The assistant text content.

    Raises:
        RuntimeError: If Groq SDK is not installed.
    """
    if Groq is None:
        raise RuntimeError("La librairie Groq n'est pas installée")

    # Create Groq client
    if cle_api:
        client = Groq(api_key=cle_api)
    else:
        client = Groq()
    
    # Perform the API call
    completion = client.chat.completions.create(
        model=modele,
        messages=messages,
        temperature=temperature,
        max_tokens=tokens_max,
    )
    
    # Extract and trim the answer
    contenu = completion.choices[0].message.content or ""
    return contenu.strip()


def reponse_de_secours(texte_utilisateur: str, domaine: str = "energy") -> str:
    """
    Generate a deterministic fallback answer when the API is unavailable.

    Args:
        texte_utilisateur: Raw user text.
        domaine: Domain tag ("energy" or "email").

    Returns:
        A simple, informative fallback reply.
    """
    texte = texte_utilisateur.lower()
    
    if domaine == "energy":
        # Tariff and invoice related keywords
        mots_cles_tarifs = ["tarif", "prix", "kwh", "augmentation", "facture"]
        if any(mot in texte for mot in mots_cles_tarifs):
            return (
                "Sans accès à l'IA, voici une indication générale : "
                "les tarifs électricité et gaz évoluent en fonction du marché, "
                "des taxes (ex. CSPE/CTA/TURPE) et de la puissance/consommation. "
                "Pour une estimation, précisez votre offre, puissance (kVA), "
                "consommation annuelle (kWh) et zone. "
                "Consultez aussi les références officielles "
                "(CRE, Enedis, GRDF, service-public)."
            )
        
        # Gas related keywords
        mots_cles_gaz = ["gaz", "m3", "pcs", "pci", "coefficient"]
        if any(mot in texte for mot in mots_cles_gaz):
            return (
                "Pour le gaz, la facturation se fait en kWh via un coefficient "
                "de conversion (m³ → kWh) dépendant du pouvoir calorifique "
                "(PCS/PCI) et de la zone. "
                "Vérifiez votre facture pour le coefficient exact "
                "et la zone GRDF."
            )
    
    # Generic fallback
    return (
        "Je n'ai pas accès au service d'IA pour le moment. "
        "Donnez plus de détails (contexte, chiffres, offre, période) "
        "et je fournirai un guide méthodologique pas à pas."
    )


def generer_reponse_ia(
    message_utilisateur: Optional[str] = None,
    *,
    prompt_systeme: Optional[str] = None,
    messages: Optional[List[Dict[str, str]]] = None,
    cle_api: Optional[str] = None,
    modele: str = MODELE_PAR_DEFAUT,
    temperature: float = TEMPERATURE_CHATBOT,
    tokens_max: int = TOKENS_MAX_CHATBOT,
    domaine_secours: str = "energy",
) -> str:
    """
    Generate an AI answer with graceful error handling and fallback.

    This is the main entry point used by the app. It attempts a Groq call and
    falls back to a deterministic answer if anything goes wrong.

    Args:
        message_utilisateur: Current user message.
        prompt_systeme: Assistant instructions.
        messages: Conversation history.
        cle_api: Groq API key.
        modele: Model name.
        temperature: Creativity level.
        tokens_max: Max generated tokens.
        domaine_secours: Fallback domain hint.

    Returns:
        The generated answer or a fallback response.
    """
    # Build the full message list
    messages_complets = construire_messages(
        message_utilisateur, prompt_systeme, messages
    )

    try:
        # Resolve API key
        cle_resolue = recuperer_cle_groq(cle_api)
        
        # If no key and Groq SDK missing, use fallback
        if not cle_resolue and Groq is None:
            return reponse_de_secours(
                message_utilisateur or "", domaine=domaine_secours
            )
        
        # Ensure a default model
        if not modele:
            modele = MODELE_PAR_DEFAUT
        
        # Perform the Groq call
        return appeler_groq(
            messages=messages_complets,
            modele=modele,
            temperature=temperature,
            tokens_max=tokens_max,
            cle_api=cle_resolue,
        )
        
    except Exception:
        # On any exception, return fallback answer
        return reponse_de_secours(
            message_utilisateur or "", domaine=domaine_secours
        )


def generer_reponse_email(
    texte_email: str,
    *,
    ton: str = "professionnel",
    langue: str = "fr",
    instructions_supplementaires: Optional[str] = None,
    cle_api: Optional[str] = None,
    modele: str = MODELE_PAR_DEFAUT,
    temperature: float = TEMPERATURE_EMAIL,
    tokens_max: int = TOKENS_MAX_EMAIL,
) -> str:
    """
    Generate an email reply using the requested tone and language.

    Args:
        texte_email: Incoming email body.
        ton: Requested tone (e.g., "professionnel").
        langue: "fr" or "en".
        instructions_supplementaires: Optional extra constraints.
        cle_api: Groq API key.
        modele: Model name.
        temperature: Creativity level.
        tokens_max: Max generated tokens.

    Returns:
        The generated email body text.
    """
    # Dictionnaire des tons disponibles
    tons_disponibles = {
        "professionnel": "professionnel et poli",
        "empathique": "empathique et rassurant",
        "ferme": "ferme mais courtois",
        "convivial": "amical et accessible",
    }
    ton_choisi = tons_disponibles.get(
        ton.lower(), tons_disponibles["professionnel"]
    )

    # Dictionnaire des langues
    langues_disponibles = {"fr": "en français", "en": "in English"}
    langue_choisie = langues_disponibles.get(
        langue.lower(), langues_disponibles["fr"]
    )

    # Instructions pour l'IA (adaptées à la langue demandée)
    if langue.lower() == "en":
        prompt_systeme = (
            "You are an assistant who writes clear, concise and well-structured "
            "email replies. Use the requested tone. Answer strictly in English. "
            "Return only the email body in plain text. Prefer short paragraphs "
            "and bullet points when useful."
        )
    else:
        prompt_systeme = (
            "Tu es un assistant qui rédige des réponses d'e-mails claires, "
            "concises et structurées. Respecte le ton demandé, garde un style "
            "professionnel, et fournis seulement le corps de l'e-mail sans "
            "balises techniques ni mise en forme riche. Utilise des paragraphes "
            "courts et, si utile, des puces."
        )

    # Construction du message utilisateur (adapté à la langue)
    if langue.lower() == "en":
        message_utilisateur = (
            f"Write the reply {langue_choisie}, tone {ton_choisi}.\n"
            f"Incoming email:\n---\n{texte_email}\n---\n"
        )
        prefix_contraintes = "Additional constraints: "
    else:
        message_utilisateur = (
            f"Rédige une réponse {langue_choisie}, ton {ton_choisi}.\n"
            f"E-mail reçu:\n---\n{texte_email}\n---\n"
        )
        prefix_contraintes = "Contraintes supplémentaires: "
    
    # Ajout des instructions supplémentaires si présentes
    if instructions_supplementaires and instructions_supplementaires.strip():
        message_utilisateur += (
            f"{prefix_contraintes}"
            f"{instructions_supplementaires.strip()}\n"
        )

    # Génération de la réponse
    return generer_reponse_ia(
        message_utilisateur=message_utilisateur,
        prompt_systeme=prompt_systeme,
        messages=None,
        cle_api=cle_api,
        modele=modele,
        temperature=temperature,
        tokens_max=tokens_max,
        domaine_secours="email",
    )


