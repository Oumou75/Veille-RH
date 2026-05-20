import os
import json
import requests
from datetime import datetime

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY manquant")

TODAY = datetime.now().strftime("%d/%m/%Y")

PROMPT = """Tu es un expert en droit social français. Effectue une veille RH pour le """ + TODAY + """.
Conventions collectives : IDCC 2198 (VAD) et IDCC 1501 (Restauration Rapide).
Utilise la recherche Google. Réponds UNIQUEMENT en JSON valide sans markdown.
Structure :
{
  "smic":      {"titre":"...","resume":"...","points":["..."],"date_effet":"...","source":"..."},
  "secu":      {"titre":"...","resume":"...","points":["..."],"date_effet":"...","source":"..."},
  "vad":       {"titre":"...","resume":"...","points":["..."],"date_effet":"...","source":"..."},
  "resto":     {"titre":"...","resume":"...","points":["..."],"date_effet":"...","source":"..."},
  "sejour":    {"titre":"...","resume":"...","points":["..."],"date_effet":"...","source":"..."},
  "sante":     {"titre":"...","resume":"...","points":["..."],"date_effet":"...","source":"..."},
  "formation": {"titre":"...","resume":"...","points":["..."],"date_effet":"...","source":"..."},
  "conges":    {"titre":"...","resume":"...","points":["..."],"source":"..."},
  "legis":     {"titre":"...","resume":"...","points":["..."],"source":"..."}
}
- smic : SMIC horaire et mensuel brut 35h, date revalorisation, impact IDCC 2198 et 1501
- secu : plafond SS 2026, taux cotisations patronales/salariales, IJSS
- vad : derniers avenants IDCC 2198, grille salaires
- resto : derniers avenants IDCC 1501, grille salaires, nuit/dimanche
- sejour : titres autorisant le travail, obligations employeur, sanctions, OFII
- sante : DUERP, visites medicales, AT/MP, inaptitude
- formation : CPF, OPCO Commerce, alternance, aides apprentis
- conges : jurisprudence CP, conges maternite/paternite, IDCC 2198 et 1501
- legis : 2-3 actualites legislatives RH majeures recentes
JSON valide uniquement."""


def call_gemini(prompt, api_key):
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=" + api_key
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}],
        "generationConfig": {"temperature": 0.1, "maxOutputTokens": 8192},
    }
    print("Appel Gemini...")
    response = requests.post(url, json=body, timeout=120)
    response.raise_for_status()
    raw = response.json()
    candidates = raw.get("candidates", [])
    if not candidates:
        raise ValueError("Aucune reponse")
    parts = candidates[0].get("content", {}).get("parts", [])
    full_text = "".join(p.get("text", "") for p in parts if "text" in p)
    cleaned = full_text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        cleaned = "\n".join(lines[1:-1] if lines[-1] == "```" else lines[1:])
    return json.loads(cleaned)


def main():
    print("Veille RH " + TODAY)
    data = call_gemini(PROMPT, API_KEY)
    print("OK - " + str(len(data)) + " sections")
    output = {
        "timestamp": datetime.now().isoformat(),
        "date_fr": TODAY,
        "data": data,
    }
    os.makedirs("data", exist_ok=True)
    with open("data/veille.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print("Sauvegarde OK")


if __name__ == "__main__":
    main()
