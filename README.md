# AutomaticCheck — Panier intelligent RFID

AutomaticCheck est un prototype de caisse autonome : un tag RFID lu par un ESP32 ou un lecteur série est associé à un produit SQLite, puis ajouté (ou retiré) d’un panier consultable sur téléphone.

> La documentation complète, présentée comme un site navigable, se trouve dans [`docs/site/index.html`](docs/site/index.html). Ouvrir ce fichier dans un navigateur suffit.

## Démarrage rapide

```powershell
cd AutomaticCheck
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python create_db.py
python backend.py
```

Ouvrir ensuite `http://localhost:5000`. Depuis un téléphone sur le même Wi-Fi : `http://ADRESSE_IP_DU_PC:5000`.

## Fonctionnalités réelles

- lecture d’UID RFID sur un port série configurable ;
- recherche du produit dans SQLite ;
- ajout/retrait au scan et protection contre les lectures répétées ;
- interface mobile responsive, panier et écran de paiement ;
- simulation de scan pour les démonstrations sans matériel.

## Configuration RFID

Par défaut, le service attend `COM4` à `115200` bauds. Pour changer sans modifier le code :

```powershell
$env:RFID_PORT = 'COM5'
$env:RFID_BAUD = '115200'
python backend.py
```

Le sketch ESP32 est dans `Code_Arduino/panieer_copy_20260904113013/`.

## Arborescence

```text
AutomaticCheck/                 application Flask
  backend.py                    API, panier en mémoire et lecteur RFID
  create_db.py                  initialisation des produits SQLite
  frontend/                     interface mobile HTML/CSS/JavaScript
  app.py                        ancienne interface locale Tkinter
Code_Arduino/                   programme ESP32 + MFRC522
docs/                           cahier des charges, guides et site de documentation
```

## Points d’attention

Ce prototype ne déclenche **pas un paiement bancaire réel** et ne gère pas encore les stocks, les comptes utilisateurs ou l’historique des ventes. Le bouton de paiement vide le panier en mémoire et affiche une confirmation. Les frais de 2 % sont actuellement calculés uniquement dans le navigateur ; ils ne sont pas contrôlés par le serveur.

## Documentation

- [Site de documentation](docs/site/index.html)
- [Cahier des charges](docs/CAHIER_DES_CHARGES_AUTOMATICCHECK.md)
- [Guide d’installation et d’exploitation](docs/GUIDE_UTILISATION_AUTOMATICCHECK.md)
- [Déploiement GitHub Pages](docs/DEPLOIEMENT_GITHUB_PAGES.md)
