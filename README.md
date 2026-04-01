# Caisse Automatique Intelligente

Système de caisse qui reconnaît automatiquement les produits déposés devant une caméra, calcule le montant total et génère un reçu PDF — sans scan de code-barres.

Le projet complet se trouve dans le dossier `Caisse/`.

## Démarrage rapide

```bash
cd Caisse
copy .env.example .env       # Windows
# cp .env.example .env       # Linux/Mac
docker compose up --build
```

Application : **http://localhost:3000**

Voir [Caisse/README.md](Caisse/README.md) pour le guide complet.
