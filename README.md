# Power & Gas Assistant (Streamlit + Groq)

Multipage Streamlit application featuring:
- Energy Chatbot for electricity & gas (tariffs, taxes, indexes, off‑peak hours, etc.)
- AI‑powered email reply generator

## 1) Installation
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 2) Groq configuration (free tier with quotas)
Create an API key at `https://console.groq.com`, then either export it:
```bash
export GROQ_API_KEY="gsk_..."
```
or use Streamlit secrets in `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "gsk_..."
```
In the UI (sidebar), choose a model (e.g., `llama-3.1-8b-instant`).

## 3) Run locally
```bash
streamlit run app.py
```

Pages available from the left menu:
- Energy Chatbot
- Email Replies

## 4) Deploy to Streamlit Community Cloud

1. Create a GitHub repository and push the project:
```bash
git init
git add .
git commit -m "Initial commit: Power & Gas Assistant"
git branch -M main
git remote add origin https://github.com/<your-user>/<your-repo>.git
git push -u origin main
```

2. Go to `https://share.streamlit.io`, connect your GitHub, then set:
   - Repo: `<your-user>/<your-repo>`
   - Branch: `main`
   - Main file path: `app.py`
   - Python version: 3.9+ (or your environment’s)
   - Secrets: add `GROQ_API_KEY = "gsk_..."`

3. Click Deploy. The pages `pages/01_Chatbot.py` and `pages/02_Emails.py` are auto‑discovered.

## Notes
- If no key is set or the API fails, a deterministic fallback answer is returned.
- For sensitive or changing data, verify with official sources (CRE, Enedis, GRDF, Service‑public).
