# automaticCHECK

Caisse automatique intelligente — reconnaît les produits par caméra, génère un panier et produit une facture PDF.

---

## Prérequis

| Outil | Vérification |
|-------|-------------|
| [Docker Desktop](https://www.docker.com/products/docker-desktop/) | `docker --version` |
| [Git](https://git-scm.com/) | `git --version` |

> C'est tout. Python et Node.js ne sont **pas** requis sur votre machine.

---

## Lancement en 3 commandes

```bash
# 1. Cloner le dépôt
git clone <URL_DU_DEPOT>
cd Caisse-automatique/Caisse

# 2. (Première fois) Copier le fichier d'environnement
copy .env.example .env

# 3. Construire et démarrer tous les services
docker compose up --build
```

L'application est prête quand vous voyez :
```
automaticcheck_backend  | INFO:     Application startup complete.
```

| Service | URL |
|---------|-----|
| **Application** | http://localhost:3000 |
| **API Swagger** | http://localhost:8000/docs |

---

## Connexion par défaut

| Champ | Valeur |
|-------|--------|
| Identifiant | `admin` |
| Mot de passe | `admin123` |

---

## Commandes utiles

```bash
# Lancer en arrière-plan (sans bloquer le terminal)
docker compose up --build -d

# Voir les logs en temps réel
docker compose logs -f

# Logs d'un seul service
docker compose logs -f backend

# Arrêter les conteneurs
docker compose down

# Arrêter ET supprimer les données (reset complet)
docker compose down -v

# Reconstruire après modification du code
docker compose up --build
```

---

## Structure du projet

```
Caisse/
├── backend/
│   ├── Dockerfile          ← Image du backend FastAPI
│   ├── requirements.txt
│   └── app/                ← Code FastAPI (routes, modèles, IA)
├── frontend/
│   ├── Dockerfile          ← Image nginx (build React + proxy)
│   ├── nginx.conf          ← Config nginx (proxy /api, /ws, /uploads)
│   └── src/                ← Code React
├── db/
│   └── init.sql            ← Initialisation PostgreSQL + pgvector
├── docker-compose.yml      ← Orchestre les 3 services
├── .env                    ← Variables d'environnement (secrets)
├── .env.example            ← Template .env à copier
├── best_caisse.pt          ← Modèle YOLO entraîné (10 produits)
└── DOCUMENTATION.md        ← Documentation technique complète
```

---

## Personalisation

Toutes les variables (mots de passe, clé JWT, etc.) se trouvent dans `.env` :

```env
POSTGRES_PASSWORD=monmotdepasse
SECRET_KEY=une-cle-longue-et-aleatoire
DEFAULT_ADMIN_PASSWORD=monmotdepasseadmin
```

Modifiez `.env` puis relancez `docker compose up --build`.

---

Pour la documentation technique complète (architecture, IA, API, base de données), voir [DOCUMENTATION.md](DOCUMENTATION.md).
