# 🗂 Veille RH DELEEV — 100% Gratuit

Mise à jour automatique **chaque dimanche à 09:00** via GitHub Actions + Gemini AI.  
**Coût total : 0 € — aucune carte bancaire requise.**

---

## ✅ Ce dont vous avez besoin (tout gratuit)

| Outil | Usage | Gratuit |
|-------|-------|---------|
| **GitHub** | Héberger le code + lancer la veille automatiquement | ✅ Toujours |
| **GitHub Pages** | Héberger le site web | ✅ Toujours |
| **Google Gemini API** | IA avec recherche Google intégrée | ✅ Quota gratuit très large |

---

## 🔑 Étape 0 — Obtenir une clé API Gemini (2 min)

1. Allez sur https://aistudio.google.com/app/apikey
2. Connectez-vous avec votre compte Google
3. Cliquez **« Create API Key »**
4. Copiez la clé (commence par `AIza…`)

> Le quota gratuit de Gemini est **15 requêtes/minute, 1 500/jour** — largement suffisant pour une veille hebdomadaire.

---

## 🚀 Déploiement (15 minutes)

### Étape 1 — Créer le dépôt GitHub

1. Allez sur https://github.com/new
2. Nom du dépôt : `veille-rh-deleev`
3. Choisissez **Public** (nécessaire pour GitHub Pages gratuit)
4. Cliquez **Create repository**

### Étape 2 — Mettre le code en ligne

Téléchargez le ZIP, dézippez-le, puis dans un terminal dans le dossier :

```bash
git init
git add .
git commit -m "Première version"
git remote add origin https://github.com/VOTRE_PSEUDO/veille-rh-deleev.git
git push -u origin main
```

> Pas de git ? Installez-le sur https://git-scm.com/downloads  
> Ou uploadez les fichiers directement sur GitHub via l'interface web.

### Étape 3 — Ajouter la clé Gemini (secret)

1. Sur votre dépôt GitHub → **Settings** → **Secrets and variables** → **Actions**
2. Cliquez **New repository secret**
3. Nom : `GEMINI_API_KEY`
4. Valeur : votre clé API Gemini (`AIza…`)
5. Cliquez **Add secret**

### Étape 4 — Activer GitHub Pages

1. Sur votre dépôt → **Settings** → **Pages**
2. Source : **Deploy from a branch**
3. Branch : `main` / `/ (root)`
4. Cliquez **Save**
5. Votre site sera accessible sur : `https://VOTRE_PSEUDO.github.io/veille-rh-deleev`

### Étape 5 — Lancer la première veille manuellement

1. Sur votre dépôt → onglet **Actions**
2. Cliquez sur **🔄 Veille RH Hebdomadaire**
3. Cliquez **Run workflow** → **Run workflow**
4. Attendez ~2 minutes
5. Actualisez votre site → les données apparaissent ✅

---

## 🕐 Fonctionnement automatique

Le fichier `.github/workflows/veille.yml` configure l'exécution automatique :

```yaml
schedule:
  - cron: "0 7 * * 0"   # Dimanche 07:00 UTC = 09:00 Paris (été)
```

> **En hiver (CET, UTC+1)** : le cron se déclenche à 08:00 Paris.  
> Pour déclencher à 09:00 toute l'année : changez `"0 7 * * 0"` en `"0 8 * * 0"`.

---

## 💰 Récapitulatif des coûts

| Service | Coût mensuel |
|---------|-------------|
| GitHub (code + cron) | **0 €** |
| GitHub Pages (hébergement) | **0 €** |
| Google Gemini API (4 veilles/mois) | **0 €** |
| **TOTAL** | **0 €** |

---

## 🔧 Personnalisation

- **Ajouter une thématique** : modifiez `CATEGORIES` dans `index.html` et le `PROMPT` dans `scripts/generate_veille.py`
- **Changer l'heure** : modifiez `schedule` dans `.github/workflows/veille.yml`
- **Voir les logs** : GitHub → Actions → cliquez sur le dernier run

---

*Développé pour DELEEV — IDCC 2198 (VAD) & IDCC 1501 (Restauration Rapide)*
