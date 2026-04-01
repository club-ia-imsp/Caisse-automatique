# automaticCHECK — Guide de démarrage

## Prérequis

| Outil | Version | Vérification |
|-------|---------|--------------|
| Python | 3.11 | `python --version` |
| Node.js | 18 ou 22+ | `node --version` |
| Docker Desktop | Dernière | Pour la base de données |

---

## Démarrage en 3 étapes

### Étape 1 — Démarrer la base de données (Docker)

```powershell
docker compose -f docker-compose.db.yml up -d
```

Attendre que le conteneur soit **healthy** (~10 secondes). Vérifier :

```powershell
docker ps
```

Le statut doit afficher `(healthy)`.

---

### Étape 2 — Démarrer le backend (FastAPI)

Double-cliquer sur **`start_backend.bat`**

Ou dans PowerShell :

```powershell
.\start_backend.bat
```

Le backend est prêt quand on voit :
```
INFO: Application startup complete.
```

Swagger API disponible sur : http://localhost:8000/docs

---

### Étape 3 — Démarrer le frontend (React/Vite)

Double-cliquer sur **`start_frontend.bat`**

Ou dans PowerShell :

```powershell
.\start_frontend.bat
```

L'application est disponible sur : **http://localhost:3000**

---

## Connexion

| Champ | Valeur |
|-------|--------|
| Identifiant | `admin` |
| Mot de passe | `admin123` |

---

## Structure du projet

```
automaticCHECK/
├── .env                    ← Variables d'environnement
├── best_caisse.pt          ← Modèle YOLO entraîné (10 produits)
├── start_backend.bat       ← Lancer le backend
├── start_frontend.bat      ← Lancer le frontend
├── docker-compose.db.yml   ← Base de données PostgreSQL seule
│
├── backend/
│   ├── app/
│   │   ├── api/            ← Routes FastAPI
│   │   ├── models/         ← Modèles SQLAlchemy
│   │   ├── schemas/        ← Schémas Pydantic
│   │   ├── services/       ← IA (YOLO + ResNet18) + PDF
│   │   ├── utils/          ← Sécurité (hash mots de passe, JWT)
│   │   ├── config.py       ← Configuration
│   │   ├── database.py     ← Connexion PostgreSQL
│   │   └── main.py         ← Point d'entrée FastAPI
│   ├── requirements.txt    ← Dépendances Python
│   └── uploads/            ← Images des produits
│
├── frontend/
│   ├── src/
│   │   ├── components/     ← Composants réutilisables
│   │   ├── context/        ← AuthContext (gestion session)
│   │   ├── pages/          ← Pages de l'application
│   │   ├── services/       ← Client API (axios)
│   │   ├── App.jsx         ← Routeur principal
│   │   └── index.jsx       ← Point d'entrée React
│   ├── vite.config.js      ← Configuration Vite + proxy
│   └── package.json
│
└── db/
    └── init.sql            ← Script de création des tables
```

---

## En cas de problème

### Le backend ne démarre pas
- Vérifier que le conteneur Docker est bien `healthy` : `docker ps`
- Vérifier que le port 8000 n'est pas utilisé : `netstat -ano | findstr 8000`

### Le frontend affiche des erreurs de connexion
- Vérifier que le backend tourne sur le port 8000
- Ouvrir http://localhost:8000/api/health — doit retourner `{"status":"healthy"}`

### Arrêter tout
```powershell
docker compose -f docker-compose.db.yml down
# Fermer les fenêtres du backend et frontend
```
