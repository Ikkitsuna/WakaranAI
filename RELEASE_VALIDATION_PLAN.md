# Plan de Validation Par Phases

Ce document définit les critères de réussite minimaux pour aligner les prochaines versions sur des objectifs mesurables de performance, d'automatisation CI et de validation multiplateforme.

## Phase 1 — Objectifs de performance temps réel
- **Temps de démarrage** : < 10 s entre l'exécution du binaire et la disponibilité de la capture/hotkey (mesuré sur 5 runs, moyenne et max).
- **Latence OCR/Vision (mode Fast)** : < 800 ms pour la chaîne « capture → OCR → sortie brut » sur une zone 1080p, mesurée hors traduction LLM.
- **Taux de capture réussie** : ≥ 98 % sur un jeu de 100 captures (pas de crash, pas d'overlay bloqué, texte détectable retourné).

## Phase 2 — CI obligatoire
- **Installation automatique** : la pipeline CI installe les dépendances (requirements.txt + dépendances OCR) sur un runner propre.
- **Test OCR simulé** : un test headless charge une image d'exemple et vérifie qu'une chaîne non vide est renvoyée par l'OCR (mode Fast).
- **Binaire portable** : la pipeline produit un artefact exécutable (ex. PyInstaller) prêt à être téléchargé.

## Phase 3 — Validation multiplateforme
- **Linux** : au moins une distribution validée (ex. Ubuntu LTS) avec test OCR/overlay de base.
- **macOS (M-series)** : vérification sur Apple Silicon avec test OCR simulé et lancement de l'overlay.
- **Steam Deck** : test basique en mode Bureau avec capture + OCR Fast pour confirmer la compatibilité Proton/desktop.

## Suivi & Acceptation
- Chaque phase doit être tracée dans le changelog avec la date et la version.
- Les seuils sont bloquants : une release ne peut passer à la phase suivante sans respecter 100 % des critères.
- Les mesures et logs bruts (temps, taux de réussite) doivent être attachés aux artefacts CI pour audit.
