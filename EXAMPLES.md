# 🎯 Exemples d'utilisation - Game Translator

## Cas d'usage réels

### 1. Traduire un RPG japonais

**Problème** : Vous jouez à un JRPG non traduit (ex: Persona, Dragon Quest, etc.)

**Configuration recommandée** :
```json
{
  "ollama_model": "qwen2.5:3b",
  "source_lang": "ja",
  "target_lang": "fr",
  "hotkey": "F9",
  "ocr_engine": "easyocr"
}
```

**Workflow** :
1. Lancez le jeu en mode fenêtré (plus facile pour capturer)
2. Quand un dialogue apparaît, appuyez sur F9
3. Dessinez un rectangle autour du texte japonais
4. Lisez la traduction dans l'overlay

**Tips** :
- Capturez de larges zones de texte pour plus de contexte
- EasyOCR est meilleur pour les caractères japonais
- Qwen2.5 est excellent pour les langues asiatiques

---

### 2. Visual Novel (Renpy, etc.)

**Problème** : Visual novel non traduit avec beaucoup de texte

**Configuration recommandée** :
```json
{
  "ollama_model": "gemma2:2b",
  "source_lang": "ja",
  "target_lang": "fr",
  "hotkey": "F10",
  "ocr_engine": "easyocr"
}
```

**Workflow** :
1. Mode fenêtré recommandé
2. F10 pour capturer chaque nouvelle ligne de dialogue
3. L'overlay s'affiche à côté du texte

**Tips** :
- Créez une macro clavier pour automatiser : F10 → Clic → Repeat
- Capturez uniquement la zone de dialogue (pas les noms de personnages)

---

### 3. MMO coréen/chinois

**Problème** : Interface de jeu non traduite (quêtes, items, etc.)

**Configuration recommandée** :
```json
{
  "ollama_model": "qwen2.5:7b",
  "source_lang": "ko",
  "target_lang": "fr",
  "hotkey": "F9",
  "ocr_engine": "easyocr"
}
```

**Workflow** :
1. Ouvrez l'inventaire → F9 → Capturez la description d'item
2. Ouvrez le journal de quêtes → F9 → Capturez l'objectif
3. Répétez pour chaque élément d'UI

**Tips** :
- Gardez une liste des traductions fréquentes
- Capturez des screenshots pour référence future

---

### 4. Jeu rétro émulé (SNES, PS1, etc.)

**Problème** : Vous jouez à un jeu rétro non traduit sur émulateur

**Configuration recommandée** :
```json
{
  "ollama_model": "gemma2:2b",
  "source_lang": "ja",
  "target_lang": "fr",
  "hotkey": "F9",
  "ocr_engine": "easyocr"
}
```

**Setup spécial** :
1. Émulateur en mode fenêtré
2. Augmentez la résolution interne (2x ou 3x) pour améliorer l'OCR
3. Activez les filtres "sharp" (pas de blur/smoothing)

**Tips** :
- Les polices pixelisées sont difficiles pour l'OCR
- Capturez de grandes zones de texte
- Testez avec Tesseract ET EasyOCR pour voir lequel est meilleur

---

### 5. Jeux PC anciens (VN, Adventure games)

**Problème** : Vieux jeux PC japonais (années 90-2000)

**Configuration recommandée** :
```json
{
  "ollama_model": "qwen2.5:3b",
  "source_lang": "ja",
  "target_lang": "fr",
  "hotkey": "F9",
  "ocr_engine": "easyocr"
}
```

**Setup spécial** :
- Lancez le jeu avec Wine/Proton si sur Linux
- Utilisez DxWnd pour forcer le mode fenêtré
- Augmentez la résolution si possible

---

### 6. Tutoriels de jeu en anglais

**Problème** : Vous êtes débutant et les tutoriels sont en anglais

**Configuration recommandée** :
```json
{
  "ollama_model": "gemma2:2b",
  "source_lang": "en",
  "target_lang": "fr",
  "hotkey": "F9",
  "ocr_engine": "tesseract"
}
```

**Workflow** :
1. F9 quand un panneau de tutoriel apparaît
2. Capturez l'instruction
3. Lisez la traduction

**Tips** :
- Tesseract suffit pour l'anglais
- Gemma2:2b est rapide (2-3s de traduction)

---

### 7. Sous-titres de cinématiques

**Problème** : Cinématiques non traduites

**Configuration recommandée** :
```json
{
  "ollama_model": "gemma2:2b",
  "source_lang": "ja",
  "target_lang": "fr",
  "hotkey": "F9",
  "ocr_engine": "easyocr"
}
```

**Workflow** :
1. Mettez le jeu en pause pendant les sous-titres
2. F9 → Capturez
3. Lisez la traduction
4. Continuez

**Tips** :
- Difficile en temps réel (trop lent)
- Mieux pour les dialogues avec pauses

---

## Comparaison de modèles Ollama

J'ai testé plusieurs modèles sur du texte de jeu japonais → français :

| Modèle | Vitesse | Qualité | Contexte | Recommandation |
|--------|---------|---------|----------|----------------|
| `gemma2:2b` | ⚡⚡⚡ 2-3s | ⭐⭐⭐ Bon | Dialogues courts | **MVP/Rapide** |
| `llama3.2:3b` | ⚡⚡ 3-4s | ⭐⭐⭐⭐ Très bon | Dialogues moyens | Bon compromis |
| `qwen2.5:3b` | ⚡⚡ 3-5s | ⭐⭐⭐⭐⭐ Excellent | Tout type | **Meilleur pour asiatique** |
| `mistral:7b` | ⚡ 5-7s | ⭐⭐⭐⭐⭐ Excellent | Textes longs | Qualité max |

---

## Workflow recommandés

### Mode "Speed run"

Pour traduire rapidement beaucoup de dialogues :

1. **Config** : `gemma2:2b` + `tesseract` (si anglais)
2. **Hotkey** : Utilisez une touche facile (F9)
3. **Pratique** : Entraînez-vous à dessiner vite le rectangle
4. **Macro** : Créez une macro pour automatiser la répétition

### Mode "Qualité maximale"

Pour bien comprendre une histoire :

1. **Config** : `qwen2.5:7b` ou `mistral:7b` + `easyocr`
2. **Setup** : Prenez votre temps, capturez de larges zones
3. **Context** : Capturez plusieurs dialogues d'affilée
4. **Notes** : Prenez des notes des traductions importantes

### Mode "Exploration"

Pour comprendre l'UI et les menus :

1. **Config** : `gemma2:2b` + moteur adapté à la langue
2. **Méthode** : Capturez chaque élément de menu
3. **Screenshots** : Sauvegardez des captures annotées
4. **Liste** : Créez un glossaire des termes importants

---

## Astuces avancées

### 1. Améliorer la précision OCR

**Prétraitement d'image** :
- Décommentez la ligne de prétraitement dans `main.py`
- Améliore la détection sur textes flous

**Résolution** :
- Augmentez la résolution interne du jeu/émulateur
- Plus de pixels = meilleur OCR

**Contraste** :
- Les textes blancs sur fond noir sont parfaits
- Évitez les textes avec ombres complexes

### 2. Accélérer le workflow

**Hotkey alternative** :
- Utilisez une touche de souris (avec le package `mouse`)
- Ex: clic molette = capture

**Macro clavier** :
- Créez une macro pour répéter automatiquement
- Ex: F9 → Attendre 1s → Clic → Repeat

### 3. Traduire hors-ligne

Game Translator est 100% local :
- Pas besoin d'internet
- Pas de limite de requêtes
- Confidentialité totale

### 4. Combiner avec d'autres outils

**Avec Textractor** (pour VN) :
- Textractor extrait le texte directement du jeu
- Copiez le texte dans un fichier
- Utilisez l'API Ollama pour traduire en batch

**Avec OBS** (streaming) :
- OBS peut capturer et afficher l'overlay
- Streamez votre expérience avec traductions live

---

## Exemples de résultats

### Exemple 1 : Dialogue de RPG

**Texte original (japonais)** :
```
勇者よ、ついにここまで来たか。
魔王を倒すには、この伝説の剣が必要だ。
```

**Traduction (gemma2:2b)** :
```
Héros, tu es enfin arrivé jusqu'ici.
Pour vaincre le Roi Démon, tu as besoin de cette épée légendaire.
```

**Temps** : ~3 secondes

### Exemple 2 : Description d'item

**Texte original (coréen)** :
```
전설의 화염 검
공격력 +50, 화염 피해 +30
특수 능력: 불타는 베기
```

**Traduction (qwen2.5:3b)** :
```
Épée de Flamme Légendaire
Attaque +50, Dégâts de Feu +30
Capacité Spéciale : Tranchant Enflammé
```

**Temps** : ~4 secondes

### Exemple 3 : Menu de jeu

**Texte original (anglais)** :
```
Continue Game
New Game
Load Game
Settings
Exit
```

**Traduction (gemma2:2b)** :
```
Continuer la Partie
Nouvelle Partie
Charger une Partie
Paramètres
Quitter
```

**Temps** : ~2 secondes

---

## Limitations connues

1. **Textes très courts** : L'OCR peut mal détecter 1-2 caractères
2. **Polices stylisées** : Les polices fantaisie sont difficiles à lire
3. **Textes animés** : Impossible de capturer pendant l'animation
4. **Temps réel** : Trop lent pour sous-titres qui défilent
5. **Contexte limité** : Chaque traduction est indépendante

---

**Pour plus d'infos, consultez CONFIG_ADVANCED.md et README.md**
