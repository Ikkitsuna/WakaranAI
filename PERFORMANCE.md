# Guide de Performance - Game Translator

## 🎮 Optimisation pour le Gaming

### TL;DR
- **Utilisez le mode OCR** pour jouer (`translation_mode: "ocr"` dans config.json)
- **F10 pour switcher** si besoin de précision ponctuelle
- Le mode Vision est **trop lent pour du gaming temps réel**

---

## 📊 Comparaison des Modes

| Critère | Mode OCR | Mode Vision |
|---------|----------|-------------|
| **Vitesse moyenne** | 2-5 secondes | 10-30 secondes |
| **Usage GPU** | Minimal (~5%) | Élevé (30-50%) |
| **Impact FPS jeu** | Négligeable | Peut causer des drops |
| **Précision texte clair** | ✅ Excellente | ✅✅ Excellente |
| **Précision texte stylisé** | ⚠️ Variable | ✅✅ Meilleure |
| **Contexte visuel** | ❌ Non | ✅ Oui |
| **Idéal pour** | Gaming actif | Screenshots, jeu en pause |

---

## ⚡ Recommandations par Scénario

### 🎯 Gaming actif (recommandé)
```json
{
  "translation_mode": "ocr",
  "ollama_model": "gemma2:2b"
}
```
- Traduction rapide (2-5s)
- GPU libre pour le jeu
- Parfait pour dialogues, quêtes, menus

**Workflow** :
1. Joue normalement
2. F9 sur zone à traduire
3. Continue à jouer pendant la traduction
4. Overlay affiche le résultat

---

### 📸 Screenshots / Jeu en pause
```json
{
  "translation_mode": "vision",
  "vision_model": "gemma3:4b"
}
```
- Meilleure précision
- Comprend le contexte visuel
- Gère mieux les polices stylisées

**Workflow** :
1. Met le jeu en pause
2. F9 sur zone à traduire
3. Attend 10-30s
4. Précision maximale

---

### 🔄 Mode Hybride (flexible)
Commence en OCR, bascule en Vision si besoin :

1. **Par défaut** : Mode OCR (`config.json`)
2. **Si texte mal détecté** : Appuie sur **F10** pour passer en Vision
3. **Pour revenir** : Appuie à nouveau sur **F10**

```
Gaming normal → OCR (rapide)
              ↓ F10
Texte complexe → Vision (précis)
              ↓ F10
Gaming normal → OCR (rapide)
```

---

## 🖥️ Configuration Matérielle

### RTX 3070 / RTX 3060 / RTX 4060
- **Gaming + OCR** : ✅ Parfait, aucun lag
- **Gaming + Vision** : ⚠️ Possible lag, FPS drops
- **Recommandation** : OCR par défaut, Vision seulement en pause

### RTX 4070+ / RTX 4090
- **Gaming + OCR** : ✅ Parfait
- **Gaming + Vision** : ✅ OK si jeu pas ultra gourmand
- **Recommandation** : OCR pour sécurité, Vision possible

### GPU < RTX 3060
- **Gaming + OCR** : ✅ OK
- **Gaming + Vision** : ❌ Lag garanti
- **Recommandation** : OCR uniquement

---

## 🚀 Optimisations Supplémentaires

### 1. Choisir un modèle plus léger pour OCR
Si `gemma2:2b` est encore trop lent :
```bash
ollama pull qwen2.5:1.5b
```
Puis dans `config.json` :
```json
{
  "ollama_model": "qwen2.5:1.5b"
}
```

### 2. Réduire la zone capturée
Plus petite zone = traitement plus rapide
- Capture juste la ligne de dialogue
- Évite de capturer tout l'écran

### 3. Résolution de capture
Le code capture à la résolution native. Si jeu en 4K :
- Passe le jeu en 1080p pour réduire la charge
- Ou capture des zones plus petites

### 4. Fermer applications en arrière-plan
- Navigateur avec onglets lourds
- Streams Twitch/YouTube
- Autres jeux / launchers

---

## 🔍 Debugging Performance

### Mesurer les temps
Le programme affiche les temps :
```
⏱️ OCR terminé en 0.32s
⏱️ Traduction terminée en 3.84s
```

Si trop lent :
1. **OCR > 1s** : Zone trop grande ou Tesseract lent
2. **Traduction > 10s** : Modèle trop lourd ou Ollama surchargé

### Vérifier l'usage GPU
Pendant le jeu :
```powershell
# Ouvrir Task Manager → Performance → GPU
```

- Jeu seul : 70-90%
- Jeu + OCR : 72-92% (minimal)
- Jeu + Vision : 90-100% (risque lag)

---

## 💡 Astuces Pro

1. **Bind sur manette** : Utiliser un logiciel comme JoyToKey pour mapper F9 sur une touche manette
2. **Second écran** : Si dual screen, overlay sur écran 2 pour ne pas gêner
3. **Hotkey personnalisée** : Change `"hotkey": "F9"` si conflit avec le jeu
4. **Cache traductions** : À venir dans future version pour dialogues récurrents

---

## ❓ FAQ Performance

**Q: Mode Vision est lent, normal ?**  
A: Oui ! Modèle vision = 3.3GB à charger en VRAM. OCR est 100x plus rapide.

**Q: Puis-je utiliser CPU au lieu de GPU ?**  
A: Ollama utilise GPU par défaut. CPU possible mais encore + lent.

**Q: Overlay lag le jeu ?**  
A: Non, overlay est une simple fenêtre tkinter, négligeable.

**Q: Combien de VRAM nécessaire ?**  
A: OCR mode: ~2GB | Vision mode: ~4-5GB

**Q: Mon jeu crash avec Vision mode ?**  
A: VRAM saturée. Passe en OCR ou ferme applications en arrière-plan.

---

## 📝 Résumé

| Situation | Mode recommandé | Temps | Qualité |
|-----------|----------------|-------|---------|
| Gaming action | OCR | 2-5s | ⭐⭐⭐⭐ |
| Gaming chill | OCR | 2-5s | ⭐⭐⭐⭐ |
| Jeu en pause | Vision | 10-30s | ⭐⭐⭐⭐⭐ |
| Screenshot | Vision | 10-30s | ⭐⭐⭐⭐⭐ |
| Texte stylisé | Vision | 10-30s | ⭐⭐⭐⭐⭐ |

**Règle d'or** : Si tu joues → OCR. Si tu captures → Vision.
