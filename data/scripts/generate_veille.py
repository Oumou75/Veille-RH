import os
import json
import requests
from datetime import datetime

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY manquant dans les secrets GitHub")

TODAY = datetime.now().strftime("%d/%m/%Y")

PROMPT = f"""Tu es un expert en droit social français. Effectue une veille réglementaire RH complète pour le {TODAY}.

L'entreprise applique deux conventions collectives :
- IDCC 2198 : Convention Collective Nationale de la Vente à Distance (VAD)
- IDCC 1501 : Convention Collective Nationale de la Restauration Rapide

Utilise la recherche Google pour trouver les informations les plus récentes.
Réponds UNIQUEMENT avec un objet JSON valide (sans markdown, sans texte avant ou après).

Structure JSON exacte attendue :
{{
  "smic":      {{ "titre":"...", "resume":"...", "points":["...","..."], "date_effet":"...", "source":"..." }},
  "secu":      {{ "titre":"...", "resume":"...", "points":["...","..."], "date_effet":"...", "source":"..." }},
  "vad":       {{ "titre":"...", "resume":"...", "points":["...","..."], "date_effet":"...", "source":"..." }},
  "resto":     {{ "titre":"...", "resume":"...", "points":["...","..."], "date_effet":"...", "source":"..." }},
  "sejour":    {{ "titre":"...", "resume":"...", "points":["...","..."], "date_effet":"...", "source":"..." }},
  "sante":     {{ "titre":"...", "resume":"...", "points":["...","..."], "date_effet":"...", "source":"..." }},
  "formation": {{ "titre":"...", "resume":"...", "points":["...","..."], "date_effet":"...", "source":"..." }},
  "conges":    {{ "titre":"...", "resume":"...", "points":["...","..."], "source":"..." }},
  "legis":     {{ "titre":"...", "resume":"...", "points":["...","..."], "source":"..." }}
}}

Contenu attendu :
- smic : SMIC horaire et mensuel brut 35h, date dernière revalorisation, prochaine prévue, impact minima IDCC 2198 et 1501
- secu : plafond SS annuel/mensuel 2026, taux cotisations patronales/salariales, IJSS
- vad : derniers avenants IDCC 2198, grille de salaires, arrêtés d'extension récents
- resto : derniers avenants IDCC 1501, grille de salaires, spécificités (nuit, dimanche, coupures)
- sejour : titres de séjour autorisant le travail, obligations employeur, sanctions, actualités, OFII
- sante : actualités santé travail 2025-2026, DUERP, visites médicales, AT/MP, inaptitude
- formation : CPF 2025-2026, OPCO Commerce, alternance, aides apprentis, CSA
- conges : jurisprudence CP récente, maternité/paternité/parental, IDCC 2198 et 1501
- legis : 2-3 actualités législatives ou jurisprudentielles RH majeures récentes

JSON valide uniquement."""

def call_gemini(prompt, api_key):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={api_key}"
    )
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 8192},
    }
    print("Appel API Gemini avec recherche Google...")
    response = requests.post(url, json=body, timeout=120)
    response.raise_for_status()
    raw = response.json()
    candidates = raw.get("candidates", [])
    if not candidates:
        raise ValueError("Aucune réponse de Gemini")
    parts = candidates[0].get("content", {}).get("parts", [])
    full_text = "".join(p.get("text", "") for p in parts if "text" in p)
    if not full_text.strip():
        raise ValueError("Réponse vide de Gemini")
    cleaned = full_text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
    return json.loads(cleaned)

def main():
    print(f"Veille RH — {TODAY}")
    data = call_gemini(PROMPT, API_KEY)
    print(f"Données reçues — {len(data)} sections")
    output = {
        "timestamp": datetime.now().isoformat(),
        "date_fr": TODAY,
        "data": data,
    }
    os.makedirs("data", exist_ok=True)
    with open("data/veille.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("Fichier data/veille.json mis à jour")

if
