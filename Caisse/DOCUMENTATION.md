# automaticCHECK — Documentation Technique Complète

## Table des matières

1. [Vue d'ensemble du projet](#1-vue-densemble)
2. [Architecture globale](#2-architecture-globale)
3. [Stack technologique](#3-stack-technologique)
4. [Base de données](#4-base-de-données)
5. [Backend FastAPI](#5-backend-fastapi)
6. [Intelligence Artificielle](#6-intelligence-artificielle)
7. [Frontend React/Vite](#7-frontend-reactvite)
8. [API — Endpoints](#8-api--endpoints)
9. [Flux d'utilisation](#9-flux-dutilisation)
10. [Configuration](#10-configuration)
11. [Sécurité](#11-sécurité)

---

## 1. Vue d'ensemble

**automaticCHECK** est une caisse automatique intelligente qui reconnaît les produits par caméra sans scan de code-barres. L'opérateur place les articles devant la caméra, le système les identifie grâce à l'IA, génère un panier et produit une facture PDF au format ticket de caisse (80 mm).

### Cas d'usage principal

```
Caméra → Détection YOLO → Identification par similarité → Panier → Facture PDF
```

---

## 2. Architecture globale

```
┌──────────────────────────────────────────────────────┐
│                   NAVIGATEUR WEB                     │
│         React 18 + Vite  (localhost:3000)            │
│  ┌────────────┐ ┌──────────┐ ┌───────────────────┐  │
│  │  Caméra   │ │  Panier  │ │  Gestion Produits │  │
│  │  WebSocket│ │  Checkout│ │  Factures         │  │
│  └────────────┘ └──────────┘ └───────────────────┘  │
└───────────────────┬──────────────────────────────────┘
                    │  HTTP/REST + WebSocket (proxy Vite)
┌───────────────────▼──────────────────────────────────┐
│              BACKEND FastAPI (localhost:8000)         │
│  ┌──────────┐ ┌───────────┐ ┌──────────┐            │
│  │ /api/auth│ │/api/prods │ │/api/inv  │            │
│  └──────────┘ └───────────┘ └──────────┘            │
│  ┌───────────────────────────────────────┐           │
│  │   AI Service: YOLO11 + ResNet18       │           │
│  │   WebSocket /ws/detection             │           │
│  └───────────────────────────────────────┘           │
└───────────────────┬──────────────────────────────────┘
                    │  asyncpg (async SQL)
┌───────────────────▼──────────────────────────────────┐
│       PostgreSQL + pgvector  (localhost:5432)         │
│   6 tables · Index HNSW · Vecteurs 512 dimensions    │
└──────────────────────────────────────────────────────┘
```

---

## 3. Stack technologique

### Backend

| Technologie | Version | Rôle |
|-------------|---------|------|
| **Python** | 3.11 | Langage principal |
| **FastAPI** | 0.104.1 | Framework API REST + WebSocket |
| **Uvicorn** | 0.24.0 | Serveur ASGI haute performance |
| **SQLAlchemy** | 2.0.23 | ORM async pour PostgreSQL |
| **asyncpg** | 0.29.0 | Driver PostgreSQL asynchrone |
| **pgvector** | 0.2.4 | Client Python pour les vecteurs pgvector |
| **ultralytics** | ≥8.1.0 | YOLO11 — détection d'objets |
| **PyTorch** (CPU) | installé avec ultralytics | Inférence ResNet18 |
| **opencv-python-headless** | 4.9.0.80 | Traitement d'images (sans GUI) |
| **fpdf2** | 2.7.9 | Génération de factures PDF |
| **python-jose** | 3.3.0 | JWT (JSON Web Tokens) |
| **passlib[bcrypt]** | 1.7.4 | Hachage des mots de passe |
| **pydantic** | 2.5.2 | Validation des données |
| **python-dotenv** | 1.0.0 | Variables d'environnement |

### Frontend

| Technologie | Version | Rôle |
|-------------|---------|------|
| **React** | 18.2.0 | Framework UI |
| **Vite** | ≥6.0.0 | Bundler ultra-rapide (remplace CRA) |
| **React Router** | 6.21.1 | Navigation SPA |
| **Axios** | ≥1.7.0 | Client HTTP (appels API) |
| **Tailwind CSS** | 3.x | Styles utilitaires |
| **@heroicons/react** | 2.x | Icônes SVG |
| **react-webcam** | 7.2.0 | Accès caméra navigateur |
| **react-hot-toast** | 2.4.1 | Notifications toast |

### Base de données

| Technologie | Rôle |
|-------------|------|
| **PostgreSQL 15** | Base de données relationnelle |
| **pgvector** | Extension vectorielle — stocke les embeddings 512-dim |
| **Docker** (ankane/pgvector) | Conteneur pré-configuré avec pgvector |

---

## 4. Base de données

### Tables

#### `admin_users` — Utilisateurs administrateurs
| Colonne | Type | Description |
|---------|------|-------------|
| `id` | UUID (PK) | Identifiant unique |
| `username` | VARCHAR(100) | Nom d'utilisateur (unique) |
| `email` | VARCHAR(255) | Email (unique) |
| `hashed_password` | VARCHAR(500) | Mot de passe haché en bcrypt |
| `is_active` | BOOLEAN | Compte actif ou désactivé |
| `created_at` | TIMESTAMP | Date de création |

#### `products` — Catalogue produits
| Colonne | Type | Description |
|---------|------|-------------|
| `id` | UUID (PK) | Identifiant unique |
| `name` | VARCHAR(255) | Nom du produit |
| `price` | DECIMAL(10,2) | Prix unitaire (2 décimales) |
| `category` | VARCHAR(100) | Catégorie |
| `stock_quantity` | INTEGER | Quantité en stock |
| `image_url` | VARCHAR(500) | URL image principale |
| `created_at` | TIMESTAMP | Date d'ajout |

#### `product_embeddings` — Vecteurs IA (cerveau de la reconnaissance)
| Colonne | Type | Description |
|---------|------|-------------|
| `id` | SERIAL (PK) | Identifiant auto-incrémenté |
| `product_id` | UUID (FK) | Référence vers `products` |
| `embedding` | **vector(512)** | Vecteur L2-normalisé ResNet18 |
| `image_path` | VARCHAR(500) | Chemin vers l'image source |
| `view_angle` | VARCHAR(50) | Angle de vue (Face/Dessus/etc.) |
| `created_at` | TIMESTAMP | Date d'ajout |

> L'index **HNSW** (cosine ops) sur cette table permet la recherche du plus proche voisin en O(log n).

#### `invoices` — Factures
| Colonne | Type | Description |
|---------|------|-------------|
| `id` | UUID (PK) | Numéro de facture |
| `total_amount` | DECIMAL(10,2) | Montant TTC |
| `tax_amount` | DECIMAL(10,2) | Montant TVA (18%) |
| `subtotal` | DECIMAL(10,2) | Montant HT |
| `payment_status` | VARCHAR(50) | `en_attente`, `payé`, `annulé` |
| `payment_method` | VARCHAR(50) | `espèces`, `carte`, etc. |
| `transaction_date` | TIMESTAMP | Date/heure de transaction |

#### `invoice_items` — Lignes de facture
| Colonne | Type | Description |
|---------|------|-------------|
| `id` | SERIAL (PK) | Auto-incrémenté |
| `invoice_id` | UUID (FK) | Référence facture |
| `product_id` | UUID (FK) | Référence produit |
| `quantity` | INTEGER | Quantité vendue |
| `unit_price` | DECIMAL(10,2) | Prix au moment de la vente (snapshot) |

#### `security_logs` — Alertes et incidents
| Colonne | Type | Description |
|---------|------|-------------|
| `id` | SERIAL (PK) | Auto-incrémenté |
| `invoice_id` | UUID (FK) | Facture concernée (nullable) |
| `issue_type` | VARCHAR(200) | Type d'alerte |
| `description` | TEXT | Détail libre |
| `is_resolved` | BOOLEAN | Résolu ou non |
| `created_at` | TIMESTAMP | Date de création |

---

## 5. Backend FastAPI

### Point d'entrée — `app/main.py`

Gère :
- Le démarrage **lifespan** : crée l'admin par défaut, initialise l'IA, crée le dossier `uploads/`
- Le middleware **CORS** (autorise `localhost:3000`)
- Le montage des fichiers statiques `/uploads`
- L'inclusion des 4 routeurs

### Configuration — `app/config.py`

Charge le fichier `.env` via `python-dotenv`. Variables accessibles via `settings.*` dans tout le projet.

### Base de données — `app/database.py`

Utilise `create_async_engine` SQLAlchemy avec un pool de connexions (pool_size=10). Fournit `get_db()` comme dépendance FastAPI injectable.

### Modèles SQLAlchemy — `app/models/`

Chaque modèle hérite de `Base` (DeclarativeBase). Les prix utilisent `Numeric(10,2)` pour éviter les erreurs d'arrondi flottant.

### Schémas Pydantic — `app/schemas/`

Séparation claire entre :
- `*Create` — données d'entrée (POST)
- `*Update` — mise à jour partielle (PUT)
- `*Response` — données de sortie (GET)

### Sécurité — `app/utils/security.py`

- `hash_password(plain)` → bcrypt
- `verify_password(plain, hashed)` → vérification
- `create_access_token(data)` → JWT HS256, expire en 480 min
- `get_current_user(token, db)` → dépendance FastAPI qui décode le JWT et retourne l'utilisateur

---

## 6. Intelligence Artificielle

### Pipeline en deux étapes

```
Image caméra (base64)
        │
        ▼
   ┌─────────┐
   │  YOLO11 │  ← best_caisse.pt (modèle personnalisé)
   └─────────┘
        │  Bounding boxes des objets détectés
        ▼
   Crop de l'objet détecté
        │
        ▼
   ┌──────────┐
   │ ResNet18 │  ← poids ImageNet (feature extractor)
   └──────────┘
        │  Vecteur 512 dimensions (L2-normalisé)
        ▼
   Recherche cosinus dans pgvector
        │  Produit le plus similaire (seuil 0.35)
        ▼
   Résultat : nom du produit + prix + score
```

### YOLO11 (`best_caisse.pt`)

- Modèle YOLOv11 **entraîné sur le stock réel** du projet
- 10 classes natives : `assiette`, `banane`, `bouteille`, `couteau`, `cuillère`, `fourchette`, `livre`, `oeuf`, `pomme`, `stylo`
- Seuil de confiance : `0.4` (détection en temps réel)
- Seuil d'entraînement : `0.3` (plus permissif pour capturer plus d'angles)
- **Pourquoi YOLO ?** Rapide (temps réel sur CPU), précis sur des objets isolés, produit des bounding boxes pour le recadrage

### ResNet18 (Feature Extractor)

- Modèle pré-entraîné ImageNet, **dernière couche de classification retirée**
- Sortie : vecteur 512 dimensions (couche avgpool)
- Normalisation L2 : tous les vecteurs ont une norme = 1
- **Pourquoi ResNet18 ?** Léger (11M paramètres), tourne en CPU, les features ImageNet généralisent bien aux objets du quotidien

### Few-Shot Learning

- Chaque produit dispose de **5 images d'entraînement** (5 angles différents)
- Chaque image génère un vecteur 512-dim stocké dans `product_embeddings`
- Au moment de la détection, la **similarité cosinus** est calculée entre l'embedding détecté et tous les embeddings stockés
- Le produit dont la moyenne des k-plus-proches est la plus haute est retenu si score > **0.35**
- **Pourquoi few-shot ?** On peut ajouter un nouveau produit avec seulement 5 photos, sans réentraîner le modèle YOLO

### WebSocket `/ws/detection`

Le frontend envoie des frames base64 toutes les 500ms via WebSocket. Le backend :
1. Décode la frame base64 → numpy array (OpenCV)
2. Passe dans YOLO → bounding boxes
3. Pour chaque détection → crop → ResNet18 → embedding
4. Cherche dans pgvector (cosine similarity)
5. Retourne JSON `{cart: [...], annotated_frame: "base64..."}`

---

## 7. Frontend React/Vite

### Pages

| Page | Route | Rôle |
|------|-------|------|
| `Login.jsx` | `/login` | Authentification JWT |
| `Dashboard.jsx` | `/` | Vue d'ensemble : stats, alertes |
| `Checkout.jsx` | `/checkout` | Caisse active + caméra + panier |
| `AdminProducts.jsx` | `/products` | Liste et gestion des produits |
| `AddProduct.jsx` | `/products/new` | Ajout produit + upload 5 images + entraînement |
| `InvoiceHistory.jsx` | `/invoices` | Historique des factures + téléchargement PDF |

### Composants

| Composant | Rôle |
|-----------|------|
| `Navbar.jsx` | Barre de navigation avec liens et bouton déconnexion |
| `CameraFeed.jsx` | Gestion WebSocket, envoi de frames, affichage annotations |
| `Cart.jsx` | Affichage du panier temps réel avec quantités et total |
| `InvoicePreview.jsx` | Aperçu de la facture générée |
| `ProtectedRoute.jsx` | Redirige vers `/login` si non authentifié |

### Gestion de l'état — `AuthContext.jsx`

Context React qui :
- Charge le token JWT depuis `localStorage`
- Vérifie sa validité au démarrage (`GET /api/auth/me`)
- Expose `{ user, loginUser, logout, isAuthenticated }`
- Clé localStorage : `automaticcheck_token` / `automaticcheck_user`

### Client API — `services/api.js`

Axios avec :
- `baseURL: '/api'` → proxied vers `http://localhost:8000/api` par Vite
- Intercepteur request : ajoute `Authorization: Bearer <token>` automatiquement
- Intercepteur response : redirige vers `/login` si 401

### Proxy Vite (`vite.config.js`)

Toutes les requêtes `/api/*`, `/ws/*` et `/uploads/*` sont **automatiquement redirigées** vers `localhost:8000`. Cela évite les problèmes CORS en développement.

---

## 8. API — Endpoints

### Authentification (`/api/auth`)

| Méthode | URL | Description | Auth requise |
|---------|-----|-------------|:---:|
| POST | `/api/auth/login` | Connexion → retourne JWT | ✗ |
| GET | `/api/auth/me` | Infos utilisateur connecté | ✓ |

### Produits (`/api/products`)

| Méthode | URL | Description | Auth requise |
|---------|-----|-------------|:---:|
| GET | `/api/products/` | Liste tous les produits | ✗ |
| GET | `/api/products/{id}` | Détails d'un produit | ✗ |
| POST | `/api/products/` | Créer un produit | ✓ |
| PUT | `/api/products/{id}` | Modifier un produit | ✓ |
| DELETE | `/api/products/{id}` | Supprimer un produit | ✓ |
| POST | `/api/products/{id}/train` | Uploader des images d'entraînement | ✓ |
| GET | `/api/products/{id}/embeddings` | Voir les embeddings d'un produit | ✓ |

### Factures (`/api/invoices`)

| Méthode | URL | Description | Auth requise |
|---------|-----|-------------|:---:|
| GET | `/api/invoices/` | Historique des factures | ✓ |
| GET | `/api/invoices/{id}` | Détails d'une facture | ✓ |
| POST | `/api/invoices/` | Créer une facture (finalise un panier) | ✓ |
| PATCH | `/api/invoices/{id}/payment` | Mettre à jour le statut de paiement | ✓ |
| GET | `/api/invoices/{id}/pdf` | Télécharger la facture en PDF | ✓ |

### Détection (`/ws`)

| Type | URL | Description |
|------|-----|-------------|
| WebSocket | `/ws/detection` | Flux temps réel caméra → détections |

### Santé

| Méthode | URL | Description |
|---------|-----|-------------|
| GET | `/api/health` | Vérification que l'API répond |

> Documentation Swagger interactive : http://localhost:8000/docs

---

## 9. Flux d'utilisation

### Ajouter un nouveau produit

```
1. Se connecter (admin / admin123)
2. Menu → Produits → Ajouter
3. Remplir : nom, prix, catégorie, stock
4. Uploader 5 photos (angles variés : face, dessus, gauche, droite, arrière)
5. Cliquer "Entraîner le modèle"
   → ResNet18 extrait 5 embeddings → stockés dans product_embeddings
6. Le produit est désormais reconnaissable par la caméra
```

### Effectuer une vente

```
1. Menu → Caisse
2. Cliquer "Démarrer la caméra"
3. Poser les articles devant la caméra
   → YOLO détecte → ResNet18 identifie → ajouté au panier
4. Vérifier le panier (modifier les quantités si besoin)
5. Cliquer "Valider la commande"
6. Choisir le mode de paiement
7. La facture est créée → télécharger le PDF (ticket 80mm)
```

### Consulter l'historique

```
1. Menu → Factures
2. Voir toutes les transactions avec statut, date, montant
3. Cliquer sur une facture → aperçu ou téléchargement PDF
```

---

## 10. Configuration

Toutes les variables sont dans le fichier **`.env`** à la racine du projet.

| Variable | Valeur | Description |
|----------|--------|-------------|
| `DATABASE_URL` | `postgresql+asyncpg://foodlink:foodlink_secure_2024@localhost:5432/foodlink_db` | Chaîne de connexion PostgreSQL async |
| `SECRET_KEY` | `foodlink-super-secret-key...` | Clé de signature JWT (changer en production) |
| `ALGORITHM` | `HS256` | Algorithme JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `480` | Durée de vie du token (8 heures) |
| `DEFAULT_ADMIN_USERNAME` | `admin` | Nom d'utilisateur admin par défaut |
| `DEFAULT_ADMIN_PASSWORD` | `admin123` | Mot de passe admin par défaut |
| `YOLO_MODEL` | Chemin vers `best_caisse.pt` | Modèle YOLO à charger |
| `EMBEDDING_DIM` | `512` | Dimensions des vecteurs ResNet18 |
| `SIMILARITY_THRESHOLD` | `0.35` | Seuil minimal de similarité cosinus |
| `UPLOAD_DIR` | Chemin vers `backend/uploads` | Dossier de stockage des images |
| `POSTGRES_USER` | `foodlink` | Utilisateur PostgreSQL (Docker) |
| `POSTGRES_PASSWORD` | `foodlink_secure_2024` | Mot de passe PostgreSQL (Docker) |
| `POSTGRES_DB` | `foodlink_db` | Nom de la base de données |

---

## 11. Sécurité

### Authentification

- Tous les endpoints d'écriture (`POST`, `PUT`, `DELETE`, `PATCH`) nécessitent un token JWT valide
- Le token est envoyé dans l'en-tête HTTP : `Authorization: Bearer <token>`
- Expiration : 8 heures. L'utilisateur est redirigé vers `/login` automatiquement

### Mots de passe

- Stockés uniquement en **bcrypt** (coût algorithmique élevé, résistant au brute-force)
- Aucun mot de passe en clair dans la base de données

### Validation des données

- Toutes les entrées passent par **Pydantic** avant d'atteindre la base de données
- Protection contre les injections SQL via SQLAlchemy ORM (requêtes paramétrées)

### Fichiers uploadés

- Les extensions et types MIME sont vérifiés avant enregistrement
- Les fichiers sont stockés dans un dossier dédié hors du code source

### CORS

- Limité à `http://localhost:3000` et `http://127.0.0.1:3000` en développement

---

*Documentation générée pour automaticCHECK v1.0*
