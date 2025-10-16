# 🚀 Installation rapide - Game Translator (Windows)

## Étape 1 : Installer Python 3.10+

1. Téléchargez Python depuis : https://www.python.org/downloads/
2. **IMPORTANT** : Cochez "Add Python to PATH" pendant l'installation
3. Redémarrez votre terminal après installation
4. Vérifiez l'installation :
   ```powershell
   python --version
   ```

## Étape 2 : Installer Tesseract OCR

### Option A : Installeur automatique (recommandé)
1. Téléchargez : https://github.com/UB-Mannheim/tesseract/wiki
2. Choisissez `tesseract-ocr-w64-setup-5.x.x.exe` (64-bit)
3. Installez avec les options par défaut
4. Notez le chemin d'installation (généralement `C:\Program Files\Tesseract-OCR`)

### Option B : Avec Chocolatey (si installé)
```powershell
choco install tesseract
```

### Configuration de Tesseract

Si Tesseract n'est pas dans le PATH, ajoutez cette ligne au début de `ocr_handler.py` (ligne 8) :

```python
import pytesseract
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```

## Étape 3 : Installer Ollama

1. Téléchargez Ollama pour Windows : https://ollama.ai/download/windows
2. Installez-le
3. Ollama démarre automatiquement en arrière-plan
4. Téléchargez le modèle Gemma2 :
   ```powershell
   ollama pull gemma2:2b
   ```
5. Vérifiez qu'Ollama tourne :
   - Ouvrez http://localhost:11434 dans votre navigateur
   - Vous devriez voir "Ollama is running"

## Étape 4 : Installer les dépendances Python

```powershell
cd ProjectRosetaAI
pip install -r requirements.txt
```

**Note** : L'installation peut prendre quelques minutes (notamment pour EasyOCR et OpenCV).

## Étape 5 : Tester l'installation

Exécutez le script de test :
```powershell
python test_setup.py
```

Ce script vérifie que :
- ✅ Python est installé
- ✅ Toutes les dépendances sont installées
- ✅ Tesseract fonctionne
- ✅ Ollama est accessible
- ✅ Le modèle Gemma2 est disponible

## Étape 6 : Lancer l'application

```powershell
python main.py
```

Appuyez sur **F9** pour commencer !

---

## 🐛 Problèmes fréquents sur Windows

### "python n'est pas reconnu"
→ Python n'est pas dans le PATH. Réinstallez Python en cochant "Add to PATH" ou ajoutez-le manuellement.

### "pip n'est pas reconnu"
→ Utilisez `python -m pip install -r requirements.txt`

### Erreur "Permission denied" lors de l'installation des packages
→ Exécutez PowerShell en mode administrateur ou utilisez `pip install --user -r requirements.txt`

### "TesseractNotFoundError"
→ Tesseract n'est pas dans le PATH. Modifiez `ocr_handler.py` comme indiqué ci-dessus.

### La hotkey F9 ne fonctionne pas
→ Lancez PowerShell en mode administrateur (requis pour les hotkeys globales sur Windows)

### L'overlay n'apparaît pas
→ Vérifiez que le texte a bien été détecté dans les logs de la console

---

## 📝 Commandes utiles

```powershell
# Vérifier qu'Ollama tourne
ollama list

# Tester Tesseract
tesseract --version

# Voir les modèles Ollama disponibles
ollama list

# Relancer Ollama si besoin
ollama serve
```

---

## 🎯 Prêt à démarrer

Une fois tout installé :

1. Ouvrez PowerShell (en mode administrateur de préférence)
2. `cd ProjectRosetaAI`
3. `python main.py`
4. Lancez votre jeu
5. Appuyez sur **F9** et sélectionnez la zone à traduire !

**Bon jeu ! 🎮**
