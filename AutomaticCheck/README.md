# AutomaticCheck — application

Ce dossier contient l’application exécutable du panier intelligent RFID.

La documentation de référence est à la racine du projet :

- [README principal](../README.md) — présentation et démarrage rapide ;
- [Site de documentation](../docs/site/index.html) — documentation navigable ;
- [Cahier des charges](../docs/CAHIER_DES_CHARGES_AUTOMATICCHECK.md) ;
- [Guide d’exploitation](../docs/GUIDE_UTILISATION_AUTOMATICCHECK.md).

## Lancer

\`\`\`powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
pip install -r requirements.txt
python create_db.py
python backend.py
\`\`\`

Ouvrir ensuite http://localhost:5000.

## Répertoires et fichiers

| Élément | Rôle |
|---|---|
| backend.py | Serveur Flask, API, lecture RFID et panier mémoire |
| create_db.py | Création/mise à jour du catalogue SQLite |
| produits.db | Base locale des produits |
| frontend/ | Interface mobile servie par Flask |
| app.py | Ancienne interface Tkinter, non utilisée par le parcours web |

Le port RFID se règle sans modifier le code :

\`\`\`powershell
$env:RFID_PORT = 'COM5'
$env:RFID_BAUD = '115200'
python backend.py
\`\`\`
