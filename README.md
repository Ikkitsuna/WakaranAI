# Game Translator

Outil de traduction en temps réel pour jeux vidéo utilisant l'OCR/Vision et l'IA locale (Ollama).

Permet de traduire instantanément les textes de jeux non traduits en capturant une zone de l'écran.

## Fonctionnalités

- **Deux modes de traduction** : OCR rapide ou Vision précis
- Hotkey globale (F9) pour capturer et traduire
- Hotkey de toggle (F10) pour changer de mode en temps réel
- Sélection visuelle de la zone à traduire
- Traduction via Ollama (100% local)
- Overlay transparent avec auto-fermeture (30s)
- Configuration via fichier JSON

## 🚀 Modes de traduction

### Mode OCR (Rapide - Recommandé pour gaming)
- **Pipeline** : Screenshot → Tesseract OCR → LLM traduction
- **Vitesse** : ⚡ Très rapide (2-5 secondes)
- **Précision** : ✅ Bonne pour textes clairs
- **Usage GPU** : Minimal (bon pour gaming)
- **Idéal pour** : Jeux en cours, textes simples

### Mode Vision (Précis - Recommandé hors gaming)
- **Pipeline** : Screenshot → Vision Model → Traduction directe
- **Vitesse** : 🐌 Lent (10-30 secondes)
- **Précision** : ✅✅ Excellente, comprend le contexte visuel
- **Usage GPU** : Élevé (peut lag si jeu actif)
- **Idéal pour** : Screenshots, textes stylisés, jeu en pause

### Basculer entre les modes

**En jeu** : Appuyez sur `F10` pour changer de mode instantanément !

```
Mode OCR → F10 → Mode Vision
Mode Vision → F10 → Mode OCR
```

## Installation

### Prérequis

1. **Python 3.10+** installé
2. **Ollama** installé et lancé localement
3. **Tesseract OCR** installé (pour le mode OCR)

### 1. Installer Tesseract OCR

Téléchargez depuis [tesseract-ocr](https://github.com/UB-Mannheim/tesseract/wiki) et installez-le.

### 2. Installer Ollama et les modèles

1. Installez Ollama : [https://ollama.ai](https://ollama.ai)
2. Téléchargez les modèles :
   ```bash
   # Pour mode OCR (rapide, recommandé)
   ollama pull gemma2:2b
   
   # Pour mode Vision (précis, optionnel)
   ollama pull gemma3:4b
   ```
3. Lancez le serveur Ollama :
   ```bash
   ollama serve
   ```

### Étape 3 : Installer les dépendances Python

```bash
cd ProjectRosetaAI
pip install -r requirements.txt
```

**Note :** Si vous préférez EasyOCR à Tesseract, il est déjà dans les requirements. EasyOCR est plus précis mais plus lourd (télécharge des modèles au premier lancement).

---

## Configuration

Éditez `config.json` :

```json
{
  "translation_mode": "ocr",          // "ocr" (rapide) ou "vision" (précis)
  "vision_model": "gemma3:4b",        // Modèle pour mode vision
  "ollama_model": "gemma2:2b",        // Modèle pour mode OCR
  "ollama_url": "http://localhost:11434",
  "source_lang": "en",
  "target_lang": "fr",
  "hotkey": "F9",                     // Capturer et traduire
  "toggle_mode_hotkey": "F10",        // Changer de mode
  "ocr_engine": "tesseract"
}
```

### Choix du mode par défaut

- **Pour gaming** : `"translation_mode": "ocr"` (par défaut)
- **Pour screenshots** : `"translation_mode": "vision"`

Vous pouvez toujours changer avec F10 en temps réel !

## Utilisation

### Lancer l'application

```bash
python main.py
```

Vous devriez voir :
```
🎮 Game Translator - Initialisation...
==================================================
✅ Configuration chargée depuis 'config.json'
   Mode: OCR
   Modèle: gemma2:2b
   OCR: tesseract
   Traduction: en → fr
   Hotkey: F9
✅ Tesseract sélectionné
==================================================

🔍 Vérification de la configuration...
--------------------------------------------------
📝 Mode OCR activé
✅ Connexion Ollama OK
📦 Modèles disponibles: gemma2:2b, gemma3:4b
✅ Modèle 'gemma2:2b' trouvé
--------------------------------------------------

==================================================
✅ GAME TRANSLATOR PRÊT!
==================================================
📌 F9: Commencer une traduction
� F10: Changer de mode (vision ⇄ ocr)
📌 Ctrl+C: Quitter
   Mode actuel: OCR
==================================================
```

### Workflow

1. Lancez votre jeu
2. Appuyez sur **F9** pour capturer
3. Dessinez un rectangle sur la zone à traduire
4. Attendez la traduction (2-5s en OCR, 10-30s en Vision)
5. Lisez la traduction dans l'overlay (reste 30 secondes)
6. Si trop lent, appuyez sur **F10** pour passer en mode OCR rapide !

## Dépannage

### "Impossible de se connecter à Ollama"

- Vérifiez qu'Ollama est bien lancé : `ollama serve`
- Testez l'URL : ouvrez `http://localhost:11434` dans votre navigateur
- Vérifiez que le port 11434 n'est pas bloqué par un firewall

### "Tesseract non trouvé" ou "TesseractNotFoundError"

- Vérifiez que Tesseract est installé : `tesseract --version`
- Sur Windows, ajoutez le chemin dans le PATH ou modifiez `ocr_handler.py` :
  ```python
  pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
  ```

### "Aucun texte détecté"

- La zone sélectionnée est peut-être trop petite ou floue
- Essayez avec EasyOCR (plus précis) : changez `"ocr_engine": "easyocr"` dans `config.json`
- Le contraste du texte est peut-être trop faible

## Structure du projet

```
├── main.py           # Point d'entrée
├── screenshot.py     # Capture d'écran
├── ocr_handler.py    # OCR
├── translator.py     # Traduction
├── overlay.py        # Interface overlay
└── config.json       # Configuration
```

---

## 📝 Licence

Ce projet est un MVP à usage personnel. Libre à vous de l'adapter à vos besoins !

## Licence

MIT License - Projet personnel

## Crédits

Construit avec Ollama, Tesseract/EasyOCR et Python.
