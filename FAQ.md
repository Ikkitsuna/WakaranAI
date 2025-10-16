# ❓ FAQ - Game Translator

## Questions générales

### Qu'est-ce que Game Translator ?

Game Translator est un outil **gratuit et open source** qui permet de traduire en temps réel les textes de jeux vidéo non traduits. Il utilise :
- L'**OCR** (reconnaissance de caractères) pour extraire le texte de l'écran
- L'**IA locale** (Ollama) pour traduire le texte
- Un **overlay transparent** pour afficher la traduction

### Est-ce gratuit ?

Oui ! Tout est gratuit et local :
- ✅ Python (gratuit)
- ✅ Ollama (gratuit)
- ✅ Tesseract (gratuit)
- ✅ EasyOCR (gratuit)

**Aucun abonnement, aucun cloud, aucun coût.**

### Est-ce légal ?

Oui, c'est légal. Game Translator :
- N'a modifie pas les fichiers du jeu
- Ne pirate pas le jeu
- Ne redistribue pas de contenu protégé
- Est un outil d'accessibilité personnel

**Note** : Comme tout outil, utilisez-le de manière responsable.

### Ai-je besoin d'internet ?

**Non !** Game Translator fonctionne 100% en local :
- Ollama tourne sur votre PC
- Tesseract/EasyOCR sont locaux
- Aucune donnée n'est envoyée sur internet

Vous pouvez même l'utiliser en mode avion.

---

## Installation

### J'ai une erreur "Python non reconnu"

**Cause** : Python n'est pas dans le PATH système.

**Solution** :
1. Réinstallez Python depuis https://www.python.org/downloads/
2. **Cochez impérativement** "Add Python to PATH" pendant l'installation
3. Redémarrez votre terminal

### J'ai une erreur "TesseractNotFoundError"

**Cause** : Tesseract n'est pas installé ou pas trouvé.

**Solution** :
1. Installez Tesseract : https://github.com/UB-Mannheim/tesseract/wiki
2. Pendant l'installation, notez le chemin (ex: `C:\Program Files\Tesseract-OCR`)
3. Si l'erreur persiste, éditez `ocr_handler.py` et ajoutez en ligne 8 :
   ```python
   pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
   ```

### L'installation de EasyOCR prend beaucoup de temps

**Normal !** EasyOCR télécharge des modèles de deep learning (~500 MB).

**Solution** :
- Soyez patient (10-15 minutes selon votre connexion)
- Ou utilisez uniquement Tesseract : `"ocr_engine": "tesseract"` dans config.json

### "Impossible de se connecter à Ollama"

**Cause** : Ollama n'est pas lancé.

**Solution** :
1. Sur Windows, Ollama se lance automatiquement en arrière-plan
2. Vérifiez dans le systray (icône Ollama)
3. Testez en ouvrant http://localhost:11434 dans votre navigateur
4. Si besoin, lancez manuellement : `ollama serve`

---

## Utilisation

### La hotkey F9 ne fonctionne pas

**Causes possibles** :
1. Droits insuffisants (Windows)
2. Conflit avec une autre application
3. Clavier non-QWERTY

**Solutions** :
1. **Lancez PowerShell en mode administrateur**
2. Changez la hotkey dans `config.json` : `"hotkey": "F10"` ou `"hotkey": "F11"`
3. Vérifiez qu'aucune autre app n'utilise F9 (Discord, OBS, etc.)

### Comment annuler une sélection ?

**Appuyez sur Échap** pendant la sélection du rectangle.

### L'overlay n'apparaît pas

**Causes possibles** :
1. Aucun texte détecté par l'OCR
2. Erreur de traduction
3. Overlay hors écran (multi-moniteurs)

**Solutions** :
1. Vérifiez les logs dans la console : le texte a-t-il été détecté ?
2. Si "Aucun texte détecté", capturez une zone plus large
3. Si multi-écrans, forcez la position centrale (modifiez `overlay.py`, ligne 165)

### L'OCR ne détecte rien ou très mal

**Causes** :
- Texte trop petit
- Contraste faible
- Police stylisée/manuscrite
- Résolution trop basse

**Solutions** :
1. Capturez une zone plus large
2. Augmentez la résolution du jeu
3. Essayez EasyOCR : `"ocr_engine": "easyocr"`
4. Activez le prétraitement (décommentez ligne 76 dans `main.py`)

### La traduction est nulle/bizarre

**Causes** :
- Modèle trop petit
- Texte mal détecté par l'OCR
- Langue source mal détectée

**Solutions** :
1. Utilisez un modèle plus gros : `ollama pull mistral:7b`
2. Vérifiez le texte détecté dans les logs (c'est peut-être l'OCR qui a mal lu)
3. Essayez `qwen2.5:3b` pour les langues asiatiques
4. Capturez plus de contexte (phrase complète vs mots isolés)

### C'est trop lent !

**Temps normal** : 5-10 secondes par traduction (gemma2:2b + tesseract)

**Pour accélérer** :
1. Utilisez Tesseract au lieu d'EasyOCR
2. Utilisez `gemma2:2b` (le plus rapide)
3. Désactivez le prétraitement d'image
4. Vérifiez que votre GPU est utilisé par Ollama : `ollama ps`

### Puis-je traduire du japonais/coréen/chinois ?

**Oui !** Recommandations :
- **OCR** : Utilisez EasyOCR (bien meilleur pour l'asiatique)
- **Modèle** : Utilisez `qwen2.5:3b` ou `qwen2.5:7b` (spécialisé)
- **Config** : `"source_lang": "ja"` (ou "ko", "zh")

---

## Performances

### Quelle configuration PC minimale ?

**Minimum** :
- CPU : Intel i3 / AMD Ryzen 3 (ou équivalent)
- RAM : 8 GB
- Stockage : 5 GB (pour Ollama + modèles)

**Recommandé** :
- CPU : Intel i5 / AMD Ryzen 5
- RAM : 16 GB
- GPU : NVIDIA GTX 1060+ (pour accélérer EasyOCR et Ollama)

### Mon PC chauffe beaucoup

**Normal !** Ollama utilise le CPU/GPU intensivement.

**Solutions** :
1. Utilisez un modèle plus petit : `gemma2:2b` au lieu de `mistral:7b`
2. Fermez les autres applications lourdes
3. Améliorez le refroidissement de votre PC

### Est-ce que ça marche sur Linux/Mac ?

**Théoriquement oui**, mais non testé sur ce MVP.

**Adaptations nécessaires** :
- Installation de Tesseract : `apt-get install tesseract-ocr` (Linux) ou `brew install tesseract` (Mac)
- Les hotkeys peuvent nécessiter des droits root
- Les chemins de fichiers (remplacer `\` par `/`)

---

## Modèles Ollama

### Quel modèle choisir ?

| Besoin | Modèle recommandé |
|--------|-------------------|
| **Rapide** (anglais → français) | `gemma2:2b` |
| **Qualité** (tout type) | `mistral:7b` ou `llama3.2:7b` |
| **Asiatique** (ja/ko/zh) | `qwen2.5:3b` ou `qwen2.5:7b` |
| **Compromis** | `llama3.2:3b` |

### Comment télécharger un nouveau modèle ?

```powershell
ollama pull <nom-du-modele>

# Exemples :
ollama pull mistral:7b
ollama pull qwen2.5:3b
ollama pull llama3.2:3b
```

Puis modifiez `config.json` :
```json
{
  "ollama_model": "mistral:7b"
}
```

### Puis-je utiliser plusieurs modèles ?

Pas simultanément, mais vous pouvez :
1. Télécharger plusieurs modèles avec `ollama pull`
2. Changer le modèle dans `config.json`
3. Redémarrer l'application

### Combien d'espace disque pour les modèles ?

- `gemma2:2b` : ~1.6 GB
- `llama3.2:3b` : ~2 GB
- `qwen2.5:3b` : ~2.3 GB
- `mistral:7b` : ~4.1 GB
- `qwen2.5:7b` : ~4.7 GB

---

## Jeux spécifiques

### Est-ce que ça marche avec [nom de jeu] ?

**Ça dépend !** Critères de compatibilité :

✅ **Fonctionne bien** :
- Jeux en mode fenêtré
- Textes clairs avec bon contraste
- Dialogues qui restent affichés
- RPG, visual novels, adventure games

⚠️ **Fonctionne moins bien** :
- Jeux en plein écran exclusif (utilisez borderless)
- Textes avec effets/ombres complexes
- Polices manuscrites/stylisées
- Sous-titres qui défilent vite

❌ **Ne fonctionne pas** :
- Jeux avec anti-cheat agressif (risque de ban)
- Jeux en VR
- Textes intégrés dans des textures 3D

### Puis-je l'utiliser en stream/enregistrement ?

**Oui !** L'overlay apparaîtra dans votre capture OBS/Streamlabs.

**Tips** :
- Capturez la fenêtre du jeu + l'overlay séparément
- Positionnez l'overlay de manière esthétique

### Est-ce que je risque un ban dans les jeux en ligne ?

**Peu probable mais possible.**

Game Translator :
- ✅ Ne modifie pas la mémoire du jeu
- ✅ Ne communique pas avec le jeu
- ⚠️ Utilise une hotkey globale (détectable par certains anti-cheats)

**Recommandation** : Utilisez-le uniquement pour des jeux solo ou avec anti-cheat léger.

---

## Personnalisation

### Puis-je changer l'apparence de l'overlay ?

**Oui !** Plusieurs options disponibles :

**⏱️ Durée d'affichage** (le plus simple - via config.json) :
```json
{
  "overlay_timeout": 60  // En secondes
}
```
- **30** : Lecture rapide
- **60** : Par défaut (1 minute)
- **90-120** : Lecture lente, textes longs
- **3600** : Pratiquement jamais fermer automatiquement (1 heure)

**🎨 Couleurs** (dans `overlay.py`, lignes 60-70) :
```python
self.root.configure(bg='#1e1e1e')  # Fond noir
title_label = tk.Label(..., fg='#61dafb', bg='#1e1e1e')  # Titre bleu
```

**📐 Dimensions** (dans `main.py`, ligne ~227) :
```python
overlay_thread = threading.Thread(
    target=show_overlay_threaded,
    args=(overlay_x, overlay_y, text, translated, 500, 300, overlay_timeout),  # width, height
    daemon=True
)
```

**💡 Conseil** : Commencez par ajuster `overlay_timeout` dans `config.json`, c'est le plus simple !

### Puis-je traduire plusieurs zones simultanément ?

**Non** dans cette version MVP. Fonctionnalité future possible.

**Workaround** : Capturez une grande zone contenant plusieurs textes.

### Puis-je sauvegarder l'historique des traductions ?

**Pas dans le MVP**, mais facile à ajouter !

**Code à ajouter** dans `main.py` (ligne ~90) :
```python
# Sauvegarder dans un fichier
with open('history.txt', 'a', encoding='utf-8') as f:
    f.write(f"{text} → {translated}\n\n")
```

---

## Dépannage avancé

### L'application crash au démarrage

**Vérifiez** :
1. Python >= 3.10 : `python --version`
2. Toutes les dépendances installées : `python test_setup.py`
3. Pas de conflit de packages : créez un virtualenv

### J'ai des caractères bizarres (encoding)

**Cause** : Problème d'encodage Windows.

**Solution** : Ajoutez en haut de `main.py` :
```python
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
```

### L'overlay reste bloqué à l'écran

**Solution** : Tuez le processus Python :
```powershell
taskkill /F /IM python.exe
```

Puis relancez l'app.

### Ollama utilise trop de RAM

**Normal** pour les gros modèles (7B+).

**Solutions** :
1. Utilisez un modèle plus petit
2. Fermez les autres applications
3. Ajoutez de la RAM à votre PC

---

## Contributions et support

### Comment contribuer au projet ?

1. Fork le repo
2. Créez une branche pour votre feature
3. Testez bien vos changements
4. Soumettez une pull request

**Idées de contributions** :
- Support Linux/Mac
- Interface graphique complète
- Cache de traductions
- Export d'historique
- Tests unitaires

### Où signaler un bug ?

**Actuellement** : Créez une issue sur GitHub (si projet publié)

**Debug** :
1. Lancez avec `python main.py` et observez les logs
2. Notez l'erreur exacte
3. Vérifiez `test_setup.py`

### Où trouver de l'aide ?

1. **Documentation** : README.md, INSTALL_WINDOWS.md, CONFIG_ADVANCED.md
2. **Exemples** : EXAMPLES.md
3. **Architecture** : ARCHITECTURE.md
4. **FAQ** : Ce fichier !

---

## Problèmes de Langues

### L'OCR retourne du charabia / caractères corrompus

**Cause** : Mauvaise configuration de `ocr_languages` dans `config.json` !

Si tu captures du texte japonais avec `"ocr_languages": ["en", "fr"]`, l'OCR va halluciner et retourner n'importe quoi.

**Solution** :
1. Identifie la langue du jeu
2. Configure les bonnes langues OCR

**Exemples** :

Jeu japonais :
```json
{
  "ocr_languages": ["ja"]  // ou ["ja", "en"] si texte mixte
}
```

Jeu chinois :
```json
{
  "ocr_languages": ["ch_sim"]  // Simplifié
// ou
  "ocr_languages": ["ch_tra"]  // Traditionnel
}
```

Jeu coréen :
```json
{
  "ocr_languages": ["ko"]
}
```

**Rappel** : `ocr_languages` = langue **du texte à capturer**, pas la langue de traduction !

### EasyOCR ne détecte pas mon GPU

**Problème** : `Neither CUDA nor MPS are available - defaulting to CPU`

**Solution** : Réinstaller PyTorch avec support CUDA

```bash
# Activer ton venv Python 3.11
.\venv311\Scripts\Activate.ps1

# Désinstaller PyTorch actuel
pip uninstall torch torchvision

# Réinstaller avec CUDA 12.1 (RTX 30xx, 40xx)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

Puis relance Game Translator et vérifie qu'EasyOCR s'initialise avec GPU.

### Tesseract ne détecte pas le japonais/chinois/coréen

**Cause** : Pack de langue manquant

**Solution** :
1. Télécharge le pack : [Tesseract Language Data](https://github.com/tesseract-ocr/tessdata)
   - Japonais : `jpn.traineddata`
   - Chinois simplifié : `chi_sim.traineddata`
   - Coréen : `kor.traineddata`
2. Copie dans `C:\Program Files\Tesseract-OCR\tessdata\`
3. Configure `config.json` :
```json
{
  "ocr_languages": ["ja"]  // ou ["ko"], ["zh_sim"], etc.
}
```

**Recommandation** : Pour langues asiatiques, utilise EasyOCR (bien meilleur).

---

## Divers

### Puis-je utiliser une autre API de traduction ?

**Oui !** Vous pouvez modifier `translator.py` pour utiliser :
- DeepL API
- Google Translate API
- ChatGPT API
- etc.

**Avantages de Ollama** :
- ✅ 100% gratuit
- ✅ 100% local
- ✅ Aucune limite de requêtes

### Puis-je l'utiliser pour traduire autre chose que des jeux ?

**Oui !** Ça marche pour :
- Applications non traduites
- Sites web
- Vidéos (sous-titres)
- PDFs affichés à l'écran
- Tout ce qui s'affiche à l'écran !

### Y a-t-il une version mobile ?

**Non.** Game Translator nécessite un PC pour faire tourner Ollama.

---

**Vous avez une autre question ? Consultez la documentation ou explorez le code !**
