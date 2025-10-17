# Game Translator

Outil de traduction en temps réel pour jeux vidéo utilisant l'OCR/Vision et l'IA locale (Ollama).

Permet de traduire instantanément les textes de jeux non traduits en capturant une zone de l'écran.

## Fonctionnalités

- **Trois modes de traduction** : Tesseract (rapide), EasyOCR (précis) ou Vision (contexte)
- **Auto-détection de langue** : Détecte automatiquement la langue du texte (japonais, coréen, chinois, etc.)
- Hotkey globale (F9) pour capturer et traduire
- Hotkey de toggle (F10) pour changer de mode en temps réel
- Sélection visuelle de la zone à traduire
- Traduction via Ollama (100% local)
- Overlay transparent avec auto-fermeture configurable (60s par défaut)
- Configuration via fichier JSON

## 🚀 Modes de traduction

### 1. Mode Tesseract (Rapide ⚡)
- **Pipeline** : Screenshot → Tesseract OCR → LLM traduction
- **Vitesse** : ⚡ Très rapide (2-5 secondes)
- **Précision** : ✅ Bonne pour textes clairs
- **Usage GPU** : Minimal (bon pour gaming)
- **Idéal pour** : Jeux en cours, textes simples, langues européennes

### 2. Mode EasyOCR (Précis 🎯)
- **Pipeline** : Screenshot → EasyOCR → LLM traduction
- **Vitesse** : ⚡⚡ Rapide (5-10 secondes)
- **Précision** : ✅✅ Excellente pour langues asiatiques
- **Usage GPU** : Moyen (avec CUDA) ou CPU
- **Idéal pour** : Japonais, Coréen, Chinois, 80+ langues
- **Note** : Nécessite Python 3.11 ou 3.12

### 3. Mode Vision (Contexte 🔍)
- **Pipeline** : Screenshot → Vision Model → Traduction directe
- **Vitesse** : 🐌 Lent (10-30 secondes)
- **Précision** : ✅✅✅ Excellente, comprend le contexte visuel
- **Usage GPU** : Élevé (peut lag si jeu actif)
- **Idéal pour** : Screenshots, textes stylisés, jeu en pause

### Basculer entre les modes

**En jeu** : Appuyez sur `F10` pour cycler entre les modes !

```
Tesseract → F10 → EasyOCR → F10 → Vision → F10 → Tesseract...
```

### 🔍 Auto-détection de langue

Par défaut, le système détecte **automatiquement** la langue du texte capturé :

- ✅ **Japonais** (Hiragana, Katakana, Kanji) → Auto-configure pour `ja`
- ✅ **Coréen** (Hangul) → Auto-configure pour `ko`
- ✅ **Chinois** (caractères CJK) → Auto-configure pour `ja` (compatibilité)
- ✅ **Arabe, Russe, Cyrillique** → Auto-configurés
- ✅ **Texte mixte** → Détecte les multiples langues

**Plus besoin de configurer `ocr_languages` manuellement !**

Pour désactiver l'auto-détection, modifier `config.json` :
```json
{
  "auto_detect_language": false
}
```

## 🚀 Installation Rapide

### Option 1 : Installation automatique (Recommandée)

1. Téléchargez le projet (ZIP ou `git clone`)
2. Double-cliquez sur **`INSTALL.bat`**
3. Attendez la fin de l'installation
4. C'est prêt ! 🎉

### Option 2 : Installation manuelle

#### Prérequis

1. **Python 3.11 ou 3.12** ([Télécharger ici](https://www.python.org/downloads/))
   - ⚠️ **IMPORTANT** : Cocher "Add Python to PATH" lors de l'installation !
2. **Ollama** ([Télécharger ici](https://ollama.ai/))
3. **Tesseract OCR** ([Télécharger ici](https://github.com/UB-Mannheim/tesseract/wiki))
   - Ajouter au PATH : `C:\Program Files\Tesseract-OCR`
4. **Git** (optionnel, pour les mises à jour) ([Télécharger ici](https://git-scm.com/))

#### Étapes d'installation manuelle

```bash
# 1. Créer l'environnement virtuel
python -m venv venv311

# 2. Activer l'environnement (Windows)
venv311\Scripts\activate

# 3. Installer les dépendances
pip install -r requirements.txt
```

#### Installer Ollama et les modèles

1. Installez Ollama : [https://ollama.ai](https://ollama.ai)
2. Téléchargez les modèles :
   ```bash
   # Pour modes OCR (rapide, recommandé)
   ollama pull gemma2:2b

   # Pour mode Vision (précis, optionnel)
   ollama pull gemma3:4b
   ```
3. Lancez le serveur Ollama :
   ```bash
   ollama serve
   ```

**Note sur EasyOCR** : EasyOCR est **optionnel** mais recommandé pour :
- 🇯🇵 Jeux japonais (kanji, hiragana, katakana)
- 🇨🇳 Jeux chinois (simplifié et traditionnel)
- 🇰🇷 Jeux coréens (hangul)
- 🎨 Polices exotiques/stylisées

Pour activer EasyOCR : Décommentez les lignes dans `requirements.txt` et relancez `INSTALL.bat`

---

## ⚙️ Configuration

### Interface graphique (Recommandée)

Double-cliquez sur **`CONFIGURE.bat`** pour ouvrir l'interface de configuration et personnaliser :
- 🎯 **Raccourcis clavier** (hotkeys personnalisables)
- 🌍 **Langues** source et cible
- ⚙️ **Mode de traduction** par défaut
- ⏱️ **Durée d'affichage** de l'overlay
- 🤖 **Modèles Ollama**

### Configuration manuelle (config.json)

Vous pouvez aussi éditer directement `config.json` :

```json
{
  "translation_mode": "tesseract",
  "vision_model": "gemma3:4b",
  "ollama_model": "gemma2:2b",
  "ollama_url": "http://localhost:11434",
  "source_lang": "en",
  "target_lang": "fr",
  "ocr_languages": ["ja", "en"],
  "auto_detect_language": true,
  "hotkey": "ctrl+shift+t",
  "toggle_mode_hotkey": "ctrl+shift+m",
  "overlay_timeout": 60
}
```

### Options de configuration

- **overlay_timeout** : Durée d'affichage de l'overlay en secondes
  - Par défaut : `60` (1 minute)
  - Si vous lisez vite : `30` secondes
  - Si vous lisez lentement : `90` ou `120` secondes
  - Pour ne jamais fermer automatiquement : mettre une grande valeur comme `3600`

### Choix du mode par défaut

- **Pour gaming** : `"translation_mode": "ocr"` (par défaut)
- **Pour screenshots** : `"translation_mode": "vision"`

Vous pouvez toujours changer avec F10 en temps réel !

## 🎯 Utilisation

### Lancement rapide

Double-cliquez sur **`RUN.bat`** pour lancer Game Translator.

### Lancement manuel

```bash
# Démarrer Ollama (dans un terminal séparé)
ollama serve

# Lancer Game Translator
venv311\Scripts\python main.py
```

### Raccourcis par défaut

- **`Ctrl+Shift+T`** : Traduire une zone de l'écran
- **`Ctrl+Shift+M`** : Changer de mode (Tesseract ↔ EasyOCR ↔ Vision)
- **`Échap`** : Annuler la sélection
- **`Ctrl+C`** : Quitter l'application (dans la console)

> 💡 **Astuce** : Utilisez des combinaisons avec modificateurs (Ctrl, Shift, Alt) pour éviter les conflits avec les jeux !

### À quoi ressemble le démarrage

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
2. Appuyez sur **`Ctrl+Shift+T`** pour capturer
3. Dessinez un rectangle sur la zone à traduire
4. Attendez la traduction (2-5s en Tesseract, 5-10s en EasyOCR, 10-30s en Vision)
5. Lisez la traduction dans l'overlay (reste 60 secondes par défaut)
6. Si trop lent, appuyez sur **`Ctrl+Shift+M`** pour passer en mode Tesseract rapide !

## 🔄 Mise à jour

### Avec Git (recommandé)

Double-cliquez sur **`UPDATE.bat`** pour mettre à jour automatiquement le code et les dépendances.

### Sans Git

1. Téléchargez la dernière version depuis GitHub
2. Remplacez les fichiers (sauf `config.json`)
3. Lancez `UPDATE.bat` pour mettre à jour les dépendances

## 📁 Fichiers principaux

```
ProjectRosetaAI/
├── INSTALL.bat            # 🔧 Installation automatique
├── RUN.bat                # ▶️ Lancement rapide
├── CONFIGURE.bat          # ⚙️ Interface de configuration
├── UPDATE.bat             # 🔄 Mise à jour automatique
├── main.py                # Point d'entrée principal
├── config_gui.py          # Interface de configuration
├── config.json            # Configuration (créé au 1er lancement)
└── venv311/               # Environnement virtuel (créé par INSTALL.bat)
```

## 🐛 Dépannage

### L'overlay ne s'affiche pas
- Vérifiez que votre raccourci n'est pas utilisé par le jeu
- Essayez une combinaison avec `Ctrl+Shift+...`
- Lancez `CONFIGURE.bat` pour changer les raccourcis

### La souris reste capturée par le jeu
- Passez le jeu en **mode fenêtré** (windowed ou borderless)
- Utilisez `Échap` pour annuler la sélection
- C'est une limitation des jeux en plein écran DirectX/OpenGL

### "Impossible de se connecter à Ollama"
- Vérifiez qu'Ollama est bien lancé : `ollama serve`
- Testez l'URL : ouvrez `http://localhost:11434` dans votre navigateur
- Vérifiez que le port 11434 n'est pas bloqué par un firewall

### "Tesseract non trouvé" ou "TesseractNotFoundError"
- Vérifiez que Tesseract est installé : `tesseract --version`
- Sur Windows, ajoutez le chemin dans le PATH
- Relancez `INSTALL.bat`

### "Aucun texte détecté"
- La zone sélectionnée est peut-être trop petite ou floue
- Essayez le mode EasyOCR : `Ctrl+Shift+M` pour changer de mode
- Le contraste du texte est peut-être trop faible

### Erreur "Module not found"
- Relancez `INSTALL.bat`
- Ou manuellement : `venv311\Scripts\pip install -r requirements.txt`

### Performance lente
- Utilisez le mode **Tesseract** pour le gaming
- Vérifiez votre CPU/GPU (Vision mode est très intensif)
- Réduisez la taille de la zone sélectionnée

## 📝 TODO / Roadmap

- [ ] Support Linux/Mac
- [ ] Mode de sélection automatique (détection de zones de texte)
- [ ] Historique des traductions
- [ ] Support multi-écrans
- [ ] Interface graphique complète (sans console)
- [ ] Thèmes personnalisables pour l'overlay

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Ouvrir une issue pour signaler un bug
- Proposer une fonctionnalité
- Soumettre une pull request

## 📄 License

MIT License - Ce projet est sous licence MIT. Libre à vous de l'adapter à vos besoins !

## 🙏 Remerciements

- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [EasyOCR](https://github.com/JaidedAI/EasyOCR)
- [Ollama](https://ollama.ai/)
- [Gemma](https://ai.google.dev/gemma) (Google)

---

**Développé avec ❤️ pour la communauté gaming**

Si vous aimez ce projet, n'oubliez pas de lui donner une ⭐ sur GitHub !
