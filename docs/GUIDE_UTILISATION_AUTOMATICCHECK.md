# Guide d’installation et d’exploitation — AutomaticCheck

## Installer

Dans PowerShell, depuis le dossier `AutomaticCheck` :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python create_db.py
```

## Lancer

```powershell
python backend.py
```

Le navigateur du PC ouvre `http://localhost:5000`. Pour un téléphone, récupérer l’adresse IPv4 Wi‑Fi avec `ipconfig`, puis ouvrir `http://<IPv4>:5000` sur le même réseau.

## Tester sans RFID

Utiliser « Mode test — simuler un scan RFID » sur l’interface. Cette action appelle `POST /api/simulate_scan` et choisit un produit de démonstration.

## Connecter le lecteur

1. Brancher l’ESP32/lecteur, puis identifier son port dans le Gestionnaire de périphériques.
2. Définir le port avant de lancer le serveur : `$env:RFID_PORT = 'COM5'`.
3. Vérifier le débit : le sketch Arduino utilise `115200` bauds (`RFID_BAUD`).
4. Lancer le backend et consulter `/api/status` pour voir le statut et les ports détectés.

## Ajouter un produit

Dans `AutomaticCheck/create_db.py`, ajouter une ligne au tableau `produits` :

```python
("UID_HEXA", "Nom du produit", 1500, "Categorie", 100),
```

Puis arrêter le serveur, exécuter `python create_db.py` et le relancer. `INSERT OR REPLACE` met à jour une entrée ayant le même UID.

## Dépannage

- **Lecteur en attente :** vérifier le port COM et le câble ; ajuster `RFID_PORT`.
- **Produit inconnu :** vérifier que l’UID lu existe dans `create_db.py`, sans séparateurs.
- **Téléphone inaccessible :** vérifier le Wi‑Fi commun et l’autorisation du pare-feu Windows pour Python sur réseau privé.
- **Module introuvable :** activer l’environnement virtuel puis relancer `pip install -r requirements.txt`.

