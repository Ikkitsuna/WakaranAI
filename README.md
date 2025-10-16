# Game Translator

Outil de traduction en temps réel pour jeux vidéo utilisant l'OCR et l'IA locale (Ollama).

Permet de traduire instantanément les textes de jeux non traduits en capturant une zone de l'écran.

## Fonctionnalités

- Hotkey globale (F9 par défaut) pour activer la capture
- Sélection visuelle de la zone à traduire
- OCR avec Tesseract ou EasyOCR
- Traduction via Ollama (100% local)
- Overlay transparent avec auto-fermeture
- Configuration via fichier JSON

## Installation

### Prérequis

1. **Python 3.10+** installé
2. **Ollama** installé et lancé localement
3. **Tesseract OCR** installé (pour l'OCR)

### 1. Installer Tesseract OCR

Téléchargez depuis [tesseract-ocr](https://github.com/UB-Mannheim/tesseract/wiki) et installez-le.

### 2. Installer Ollama

1. Installez Ollama : [https://ollama.ai](https://ollama.ai)
2. Téléchargez le modèle Gemma2 (léger et performant) :
   ```bash
   ollama pull gemma2:2b
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
  "ollama_model": "gemma2:2b",
  "ollama_url": "http://localhost:11434",
  "source_lang": "en",
  "target_lang": "fr",
  "hotkey": "F9",
  "ocr_engine": "tesseract"
}
```

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
   Modèle: gemma2:2b
   Traduction: en → fr
   Hotkey: F9
   OCR: tesseract
✅ Tesseract sélectionné
==================================================

🔍 Vérification de la configuration...
--------------------------------------------------
✅ Connexion Ollama OK
📦 Modèles disponibles: gemma2:2b
✅ Modèle 'gemma2:2b' trouvé
--------------------------------------------------

==================================================
✅ GAME TRANSLATOR PRÊT!
==================================================
📌 Appuyez sur F9 pour commencer une traduction
📌 Appuyez sur Ctrl+C pour quitter
==================================================
```

1. Lancez votre jeu
2. Appuyez sur F9
3. Dessinez un rectangle sur la zone à traduire
4. Attendez 5-10 secondes
5. Lisez la traduction dans l'overlay

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
