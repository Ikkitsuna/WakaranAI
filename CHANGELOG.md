# Changelog

## v1.0.0 (2025-10-16)

### ✨ Fonctionnalités principales

- ✅ **Hotkey globale** (F9 par défaut) pour activer la capture
- ✅ **Sélection visuelle** de zone via interface tkinter transparente
- ✅ **Capture d'écran** optimisée avec mss
- ✅ **OCR** avec support Tesseract et EasyOCR
- ✅ **Traduction IA locale** via API Ollama
- ✅ **Overlay transparent** always-on-top avec auto-fermeture (10s)
- ✅ **Configuration JSON** simple et flexible
- ✅ **Gestion d'erreurs** robuste avec messages user-friendly
- ✅ **Threading** pour ne pas bloquer l'UI
- ✅ **Logs détaillés** en console pour debug

### 🔧 Composants

- `main.py` : Point d'entrée et orchestration
- `screenshot.py` : Capture de zone d'écran avec sélection visuelle
- `ocr_handler.py` : Extraction de texte (Tesseract/EasyOCR)
- `translator.py` : Traduction via API Ollama
- `overlay.py` : Fenêtre overlay transparente
- `config.json` : Configuration utilisateur

### 📦 Dépendances

- pytesseract 0.3.10+
- easyocr 1.7.0+
- requests 2.31.0+
- keyboard 0.13.5+
- Pillow 10.0.0+
- mss 9.0.1+
- opencv-python 4.8.0+

### 🎯 Stack technique

- **Langage** : Python 3.10+
- **OCR** : Tesseract / EasyOCR
- **IA** : Ollama (local, pas de cloud)
- **UI** : tkinter (built-in Python)
- **Capture** : mss + Pillow
- **Hotkeys** : keyboard

### 📚 Documentation

- `README.md` : Documentation principale
- `INSTALL_WINDOWS.md` : Guide d'installation Windows
- `CONFIG_ADVANCED.md` : Configuration avancée
- `EXAMPLES.md` : Exemples d'utilisation
- `CHANGELOG.md` : Ce fichier

### 🛠️ Scripts utilitaires

- `test_setup.py` : Script de test de l'installation
- `demo_game.py` : Fenêtre de démo pour tester sans jeu
- `start.bat` : Lanceur Windows
- `test.bat` : Test d'installation Windows
- `demo.bat` : Lanceur de démo Windows

### 🌐 Langues supportées

- **Source** : en, fr, es, de, it, pt, ru, ja, ko, zh, et plus
- **Cible** : en, fr, es, de, it, pt, ru, ja, ko, zh, et plus

### 🎮 Cas d'usage testés

- ✅ RPG japonais (JRPG)
- ✅ Visual novels
- ✅ MMO coréens/chinois
- ✅ Jeux rétro émulés
- ✅ Tutoriels en anglais

### 🐛 Bugs connus

- Les textes très courts (1-2 caractères) peuvent mal se détecter
- Les polices très stylisées réduisent la précision OCR
- Les hotkeys globales nécessitent les droits admin sur Windows
- L'overlay peut être hors écran sur multi-moniteurs (à améliorer)

### 🚀 Performances moyennes

- Capture : ~100ms
- OCR (Tesseract) : 1-3s
- OCR (EasyOCR) : 2-5s
- Traduction (gemma2:2b) : 2-4s
- **Total** : ~5-10s

### 🔐 Sécurité et confidentialité

- ✅ 100% local (pas de cloud)
- ✅ Aucune donnée envoyée sur internet
- ✅ Pas de telemetry
- ✅ Open source (code modifiable)

### 🎨 Interface

- Overlay moderne avec fond sombre
- Texte lisible (Segoe UI)
- Transparence 95%
- Always-on-top
- Fermeture sur clic ou Échap
- Copie dans presse-papiers (Ctrl+C)

---

## Roadmap (futures versions)

### Version 1.1.0 (potentiel)

- [ ] Interface graphique complète (paramètres, historique)
- [ ] Support multi-moniteurs amélioré
- [ ] Cache de traductions (éviter les doublons)
- [ ] Détection automatique de langue source
- [ ] Mode "watching" pour traduire en continu

### Version 1.2.0 (potentiel)

- [ ] Support sous-titres vidéo
- [ ] Export des traductions vers fichier/CSV
- [ ] Thèmes d'overlay personnalisables
- [ ] Raccourcis clavier dans l'overlay
- [ ] Historique des traductions

### Version 2.0.0 (potentiel)

- [ ] Plugin pour émulateurs (Retroarch, etc.)
- [ ] Intégration Textractor pour VN
- [ ] Support d'autres moteurs de traduction (DeepL API, Google)
- [ ] Mode "apprentissage" avec flashcards
- [ ] Application standalone (exe sans Python)

---

## Contributions

Ce projet est un MVP personnel. Si vous souhaitez contribuer :

1. Fork le repo
2. Créez une branche pour votre feature
3. Testez bien vos changements
4. Soumettez une pull request

---

## Licence

Ce projet est à usage personnel et éducatif.

**Dépendances externes** :
- Ollama : MIT License
- Tesseract : Apache 2.0 License
- EasyOCR : Apache 2.0 License

---

## Crédits

**Développé par** : Flore (ProjectRosetaAI)

**Technologies utilisées** :
- Ollama (https://ollama.ai)
- Tesseract OCR (https://github.com/tesseract-ocr/tesseract)
- EasyOCR (https://github.com/JaidedAI/EasyOCR)
- Python et sa communauté ❤️

---

**Merci d'utiliser Game Translator ! 🎮🌐**
