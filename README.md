# Range Battle V2 — Solo

Jeu d'entraînement aux ranges pour 6-max MTT.

## Fonctionnement

Le joueur choisit :
- profondeur : 50bb / 100bb ;
- spot ;
- action : OPEN / FOLD / RAISE.

Il peut sélectionner **plusieurs cases simultanément**, puis cliquer sur **Valider le range**.

Le programme compare la sélection au range de référence et calcule :
- nombre de bonnes cases ;
- erreurs ;
- score cumulé ;
- précision.

## Ajouter les autres ranges

Les ranges sont stockés dans `script.js`, dans l'objet `DATA`.
Le moteur est séparé des données : les captures 50bb/100bb des autres positions peuvent donc être ajoutées sans refaire l'interface.

Pour un spot OPEN, une case dans le masque vaut OPEN et une case hors masque vaut FOLD.
Les spots où RAISE est une action possible pourront utiliser un modèle à 3 actions dans une prochaine étape.

## GitHub Pages

Déposer les 3 fichiers (`index.html`, `style.css`, `script.js`) dans un repository puis activer GitHub Pages sur `main` / `/root`.
