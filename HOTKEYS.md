# 🎯 Configuration des Raccourcis Clavier

## Pourquoi changer les raccourcis ?

Les touches **F9** et **F10** peuvent être utilisées par certains jeux, ce qui cause des conflits :
- L'overlay ne s'affiche pas si le jeu capture F9
- La souris peut continuer d'interagir avec le jeu pendant la sélection

## Solution : Combinaisons de touches

Au lieu d'utiliser des touches simples, utilisez des **combinaisons** comme :
- `Ctrl+Shift+T` (par défaut pour traduire)
- `Ctrl+Shift+M` (par défaut pour changer de mode)
- `Alt+T`, `Ctrl+G`, etc.

**Avantage** : Les jeux capturent rarement les combinaisons avec modificateurs !

## Comment configurer ?

### Méthode 1 : Interface graphique (Recommandé)

1. Double-cliquez sur `configure.bat`
2. OU lancez : `python main.py --config`
3. Cliquez sur "📝 Changer" à côté du raccourci
4. Pressez la combinaison souhaitée (ex: maintenir Ctrl+Shift puis presser T)
5. Cliquez sur "💾 Sauvegarder"

### Méthode 2 : Éditer config.json manuellement

Ouvrez `config.json` et modifiez :
```json
{
  "hotkey": "ctrl+shift+t",
  "toggle_mode_hotkey": "ctrl+shift+m"
}
```

## Raccourcis recommandés

### Pour le gaming :
- `ctrl+shift+t` - Traduction (ne gêne jamais)
- `ctrl+shift+m` - Changer de mode
- `alt+t` - Alternative simple

### Si vous jouez en windowed :
- Vous pouvez garder `F9` et `F10` si ça ne pose pas de problème

## Problème de souris avec les jeux ?

La nouvelle version utilise `grab_set_global()` pour mieux capturer la souris, mais :

**Limitation Windows** : Les jeux en plein écran avec DirectX/OpenGL peuvent toujours ignorer cette capture.

**Solution** :
1. Jouez en mode **Fenêtré** ou **Fenêtré sans bordure** (au lieu de plein écran)
2. Ou utilisez `Alt+Tab` pour sortir du jeu avant d'utiliser le raccourci

## Dépannage

### L'overlay ne s'affiche pas
- Vérifiez que votre raccourci n'est pas utilisé par le jeu
- Essayez une combinaison avec `Ctrl+Shift`

### La souris reste capturée par le jeu
- Utilisez `Échap` pour annuler la sélection
- Passez en mode fenêtré dans les options du jeu

### Le raccourci ne fonctionne pas
- Vérifiez dans l'interface de configuration
- Assurez-vous que Game Translator est lancé
- Vérifiez la console pour les messages d'erreur
