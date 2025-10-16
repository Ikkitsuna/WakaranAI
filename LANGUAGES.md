# Guide des Langues - Game Translator

## 🌍 Support Multi-Langues

Game Translator supporte **3 modes OCR/Vision** avec différents niveaux de support pour les langues.

---

## 📊 Comparaison des Modes par Langue

| Langue | Tesseract | EasyOCR | Vision |
|--------|-----------|---------|--------|
| 🇬🇧 Anglais | ✅ Excellent | ✅ Excellent | ✅ Excellent |
| 🇫🇷 Français | ✅ Excellent | ✅ Excellent | ✅ Excellent |
| 🇪🇸 Espagnol | ✅ Excellent | ✅ Excellent | ✅ Excellent |
| 🇩🇪 Allemand | ✅ Excellent | ✅ Excellent | ✅ Excellent |
| 🇮🇹 Italien | ✅ Excellent | ✅ Excellent | ✅ Excellent |
| 🇵🇹 Portugais | ✅ Excellent | ✅ Excellent | ✅ Excellent |
| 🇯🇵 **Japonais** | ⚠️ Moyen* | ✅✅ Excellent | ✅✅ Excellent |
| 🇰🇷 **Coréen** | ⚠️ Moyen* | ✅✅ Excellent | ✅✅ Excellent |
| 🇨🇳 **Chinois** | ⚠️ Moyen* | ✅✅ Excellent | ✅✅ Excellent |
| 🇷🇺 Russe | ✅ Bon | ✅ Excellent | ✅ Excellent |
| 🇸🇦 Arabe | ✅ Bon | ✅ Excellent | ✅ Excellent |
| 🇹🇭 Thaï | ⚠️ Moyen | ✅ Excellent | ✅ Excellent |

**Tesseract nécessite l'installation de packs de langues*

---

## 🚀 Configuration des Langues

### Dans `config.json`

```json
{
  "translation_mode": "tesseract",
  "ocr_languages": ["en", "fr"],     // Langues pour OCR
  "source_lang": "en",                // Langue source pour traduction
  "target_lang": "fr"                 // Langue cible pour traduction
}
```

### Codes de Langues Supportés

```json
"ocr_languages": ["en"]              // Anglais uniquement
"ocr_languages": ["en", "fr"]        // Anglais + Français
"ocr_languages": ["ja"]              // Japonais uniquement
"ocr_languages": ["zh_sim"]          // Chinois simplifié
"ocr_languages": ["zh_tra"]          // Chinois traditionnel
"ocr_languages": ["ko"]              // Coréen
"ocr_languages": ["ja", "en"]        // Japonais + Anglais
```

---

## 📦 Installation des Packs de Langues Tesseract

### Windows

1. **Télécharger les packs** depuis GitHub :
   - [Tesseract Language Data](https://github.com/tesseract-ocr/tessdata)

2. **Installer le pack de langue** :
   - Téléchargez le fichier `.traineddata` (ex: `jpn.traineddata`, `kor.traineddata`)
   - Copiez-le dans : `C:\Program Files\Tesseract-OCR\tessdata\`

3. **Langues disponibles** :

| Langue | Fichier à télécharger | Code config |
|--------|----------------------|-------------|
| Japonais | `jpn.traineddata` | `ja` |
| Coréen | `kor.traineddata` | `ko` |
| Chinois Simplifié | `chi_sim.traineddata` | `zh_sim` |
| Chinois Traditionnel | `chi_tra.traineddata` | `zh_tra` |
| Russe | `rus.traineddata` | `ru` |
| Arabe | `ara.traineddata` | `ar` |
| Espagnol | `spa.traineddata` | `es` |
| Allemand | `deu.traineddata` | `de` |
| Italien | `ita.traineddata` | `it` |
| Portugais | `por.traineddata` | `pt` |

**Note** : L'anglais (`eng.traineddata`) et le français (`fra.traineddata`) sont généralement inclus par défaut.

### Vérifier les langues installées

```powershell
tesseract --list-langs
```

Devrait afficher :
```
List of available languages (3):
eng
fra
jpn
```

---

## 🎯 EasyOCR - Installation et Configuration

### Installation

**⚠️ EasyOCR nécessite Python 3.11 ou 3.12** (incompatible avec Python 3.14)

```bash
# Vérifier votre version Python
python --version

# Si Python 3.11/3.12 :
pip install easyocr opencv-python

# Si Python 3.14 :
# Utilisez Tesseract ou Vision à la place
```

### Langues Supportées par EasyOCR

EasyOCR télécharge automatiquement les modèles de langues au premier usage.

**Codes de langues** :
```python
"ocr_languages": ["en"]              # Anglais
"ocr_languages": ["ja"]              # Japonais
"ocr_languages": ["ko"]              # Coréen
"ocr_languages": ["ch_sim"]          # Chinois simplifié
"ocr_languages": ["ch_tra"]          # Chinois traditionnel
"ocr_languages": ["ja", "en"]        # Japonais + Anglais (mixte)
```

**Langues supportées** : Plus de 80 langues !
- Toutes les langues latines (en, fr, es, de, it, pt, etc.)
- Langues asiatiques (ja, ko, zh, th, vi, etc.)
- Langues avec alphabets spéciaux (ar, ru, hi, etc.)

Liste complète : https://www.jaided.ai/easyocr/

---

## 🤖 Mode Vision - Support Universel

Le mode Vision (gemma3:4b) fonctionne avec **toutes les langues** car il "voit" le texte au lieu de l'OCR.

**Avantages** :
- ✅ Aucune installation de pack de langue
- ✅ Fonctionne sur toutes les langues
- ✅ Comprend le contexte visuel
- ✅ Meilleur pour polices exotiques/stylisées

**Inconvénients** :
- ❌ Très lent (10-30 secondes)
- ❌ GPU intensif

---

## 💡 Recommandations par Cas d'Usage

### 🎮 Jeux Japonais (JRPG, Visual Novels)

**Option 1 : EasyOCR** (recommandé)
```json
{
  "translation_mode": "easyocr",
  "ocr_languages": ["ja", "en"],
  "source_lang": "ja",
  "target_lang": "fr"
}
```
- ⚡ Rapide (5-10s)
- ✅ Excellent pour caractères japonais
- ✅ Gère le mixte romaji/kanji

**Option 2 : Tesseract + Pack Japonais**
```json
{
  "translation_mode": "tesseract",
  "ocr_languages": ["ja"],
  "source_lang": "ja",
  "target_lang": "fr"
}
```
- ⚡ Plus rapide (2-5s)
- ⚠️ Moins précis sur kanji complexes
- 📦 Nécessite `jpn.traineddata`

**Option 3 : Mode Vision** (jeu en pause)
```json
{
  "translation_mode": "vision",
  "source_lang": "ja",
  "target_lang": "fr"
}
```
- 🐌 Lent (10-30s)
- ✅✅ Meilleure précision
- 🎯 Utiliser F10 pour basculer ponctuellement

---

### 🎮 Jeux Chinois

**Chinois Simplifié** (Chine continentale)
```json
{
  "translation_mode": "easyocr",
  "ocr_languages": ["ch_sim", "en"],
  "source_lang": "zh",
  "target_lang": "fr"
}
```

**Chinois Traditionnel** (Taiwan, Hong Kong)
```json
{
  "translation_mode": "easyocr",
  "ocr_languages": ["ch_tra", "en"],
  "source_lang": "zh",
  "target_lang": "fr"
}
```

---

### 🎮 Jeux Coréens

```json
{
  "translation_mode": "easyocr",
  "ocr_languages": ["ko", "en"],
  "source_lang": "ko",
  "target_lang": "fr"
}
```

---

### 🎮 Jeux Européens (Anglais/Allemand/Espagnol/etc.)

**Tesseract suffit !**
```json
{
  "translation_mode": "tesseract",
  "ocr_languages": ["en"],
  "source_lang": "en",
  "target_lang": "fr"
}
```
- ⚡⚡ Très rapide (2-4s)
- ✅ Excellente précision
- 🎮 Parfait pour gaming

---

## 🔄 Basculer entre les Modes (F10)

Pendant le jeu, tu peux cycler entre les 3 modes :

1. **Tesseract** (rapide, langues de base)
   - ⚡ 2-5 secondes
   - 🎮 Gaming actif

2. **↓ F10 ↓**

3. **EasyOCR** (précis, langues asiatiques)
   - ⏱️ 5-10 secondes
   - 🎯 Polices exotiques, japonais/chinois/coréen

4. **↓ F10 ↓**

5. **Vision** (ultra précis, tout fonctionne)
   - 🐌 10-30 secondes
   - 🤖 Contexte visuel, polices impossibles

6. **↓ F10 ↓**

7. Retour à **Tesseract**

---

## ❓ FAQ Langues

**Q: Tesseract ne détecte pas le japonais ?**  
A: Vérifie que `jpn.traineddata` est dans `C:\Program Files\Tesseract-OCR\tessdata\`

**Q: EasyOCR ne s'installe pas ?**  
A: Python 3.14 n'est pas supporté. Utilise Python 3.11 ou 3.12, ou utilise Tesseract/Vision.

**Q: Quel mode pour jeux japonais en temps réel ?**  
A: EasyOCR si Python 3.11/3.12, sinon Tesseract avec pack jpn.

**Q: Tesseract est nul en japonais, que faire ?**  
A: Passe en mode EasyOCR (F10) ou Vision (F10 x2) pour les passages difficiles.

**Q: Puis-je détecter plusieurs langues en même temps ?**  
A: Oui ! `"ocr_languages": ["ja", "en"]` détecte japonais ET anglais (utile pour jeux mixtes).

**Q: Le mode Vision fonctionne-t-il hors ligne ?**  
A: Oui, Ollama tourne en local. Aucun internet requis.

---

## 📝 Résumé

| Cas | Mode recommandé | Config |
|-----|----------------|--------|
| Jeu anglais gaming | Tesseract | `["en"]` |
| Jeu japonais gaming | EasyOCR | `["ja", "en"]` |
| Jeu chinois gaming | EasyOCR | `["ch_sim"]` |
| Jeu coréen gaming | EasyOCR | `["ko"]` |
| Police stylisée | Vision | Mode F10 x2 |
| Screenshot précis | Vision | Config vision |
| Python 3.14 | Tesseract ou Vision | Pas EasyOCR |

**Astuce Pro** : Configure Tesseract par défaut, utilise F10 pour passer en EasyOCR/Vision quand nécessaire !
