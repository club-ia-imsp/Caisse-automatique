# 🛒 FEUILLE DE ROUTE COMPLÈTE - Projet AutomaticCheck

## 📋 Table des matières
1. [Vue d'ensemble du projet](#vue-densemble)
2. [Architecture générale](#architecture)
3. [ÉTAPE 0 : Modélisation et fabrication du panier](#étape-0)
4. [ÉTAPE 1 : Préparation de l'environnement](#étape-1)
5. [ÉTAPE 2 : Mise en place de la base de données](#étape-2)
6. [ÉTAPE 3 : Développement du backend](#étape-3)
7. [ÉTAPE 4 : Développement du frontend](#étape-4)
8. [ÉTAPE 5 : Intégration RFID réelle](#étape-5)
9. [ÉTAPE 6 : Tests et validation](#étape-6)
10. [ÉTAPE 7 : Déploiement final](#étape-7)

---

## 🎯 Vue d'ensemble du projet {#vue-densemble}

**Nom du projet :** AutomaticCheck  
**Objectif :** Créer une borne de caisse automatique qui :
- Identifie automatiquement les produits via RFID (simulé sur PC)
- Génère les factures en temps réel
- Gère les modes de paiement (liquide, carte)
- Met à jour les stocks automatiquement
- Affiche tout sur une interface graphique

**Technologies utilisées :**
- **Langage principal :** Python
- **Base de données :** SQLite (simple, local, gratuit)
- **Backend/API :** FastAPI (pour servir les données)
- **Frontend :** PyQt6 ou Tkinter (interface graphique sur votre PC)
- **RFID simulation :** Lecture de codes depuis fichier ou clavier
- **Système d'exploitation :** Windows (votre ordinateur)

---

## 🏗️ Architecture générale {#architecture}

```
┌─────────────────────────────────────────────────────────┐
│              INTERFACE GRAPHIQUE (PyQt6/Tkinter)       │
│  - Affichage du panier                                  │
│  - Liste des produits                                   │
│  - Facture en temps réel                               │
│  - Choix du paiement                                    │
└────────────────┬────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────┐
│           BACKEND (FastAPI - Serveur local)             │
│  - Gestion des produits                                 │
│  - Calcul des factures                                  │
│  - Gestion des paiements                                │
│  - Mise à jour des stocks                               │
└────────────────┬────────────────────────────────────────┘
                 │
                 ↓
┌─────────────────────────────────────────────────────────┐
│         BASE DE DONNÉES (SQLite - products.db)          │
│  - Table: Produits (id, nom, prix, stock, code_rfid)   │
│  - Table: Factures (id, date, total, articles)         │
│  - Table: Paiements (id, facture_id, mode, montant)    │
└─────────────────────────────────────────────────────────┘

         ↑─────────────────────────────┘
         │ Lecture RFID réelle
         │ (lecteur USB RFID physique)
```

---

## 🏗️ ÉTAPE 0 : Modélisation et fabrication du panier {#étape-0}

### Objectif
Concevoir et imprimer le panier physique en 3D avec les antennes RFID intégrées.

### 0.1 Composants matériels nécessaires

**Pour le panier :**
- PLA ou PETG pour l'imprimante 3D (500-800g)
- 4 antennes RFID circulaires (diamètre 80mm)
- Fil de cuivre ou pistes RFID imprimées
- Adhésif double-face pour fixer les antennes

**Pour l'électronique :**
- 1× Lecteur RFID UHF ou HF (USB ou série)
  - **Recommandé :** Lecteur RFID-125kHz avec interface USB
  - **Alternative :** Module RC522 RFID (SPI)
- 1× Écran HDMI 7 pouces (ou moniteur USB)
- 1× Ordinateur Windows (déjà vous avez)
- Câbles USB (mini-USB, micro-USB)
- Alimentation 5V pour les capteurs

---

### 0.2 Modélisation 3D du panier

**Télécharger les fichiers 3D :**

#### Option 1 : Fichiers prêts à l'emploi
- Thingiverse : https://www.thingiverse.com
  - Cherchez "Smart basket", "RFID basket", "Shopping cart"
- Grabcad : https://grabcad.com
- Printables : https://www.printables.com

#### Option 2 : Concevoir votre panier

**Logiciels gratuits :**
1. **FreeCAD** (gratuit, open-source)
   - https://www.freecadweb.org/
   - Tutoriels YouTube : "FreeCAD pour débutants"

2. **Fusion 360** (gratuit pour étudiants)
   - https://www.autodesk.com/products/fusion-360
   - Inscription académique

3. **Tinkercad** (en ligne, gratuit)
   - https://www.tinkercad.com/
   - Parfait pour débuter

**Spécifications du panier à modéliser :**
```
Dimensions générales :
- Longueur : 400mm
- Largeur : 300mm
- Hauteur : 250mm
- Épaisseur des parois : 3mm

Emplacements des antennes RFID :
- 4 emplacements carrés (100mm × 100mm)
- Positionnés aux 4 coins du panier
- En retrait de 20mm des bords
- Profondeur d'encastrement : 5mm

Poignées :
- 2 poignées semi-circulaires
- Épaiseur : 15mm
- Rayon : 80mm

Grille de détection :
- Grille au fond du panier
- Espacement : 20mm
- Pour la circulation de l'air et de l'onde RFID
```

---

### 0.3 Préparer le fichier STL pour l'imprimante

**Étape par étape :**

1. **Exporter en STL**
   - Fichier → Exporter
   - Format : `.stl` (Standard Tessellation Language)
   - Résolution : 0.2mm

2. **Vérifier le fichier**
   - Ouvrir avec Cura ou PrusaSlicer (gratuit)
   - Vérifier : pas de trous, parois fermées
   - Estimer le temps d'impression

3. **Paramètres d'impression recommandés**
```
Matériau : PLA blanc ou gris
Températurebuse : 200-210°C
Plateau : 60°C
Épaisseur couche : 0.2mm (normal) ou 0.15mm (détail)
Remplissage : 15-20%
Temps estimé : 8-16 heures
Poids : 400-600g
Coût : 3-8€ selon le prix du PLA
```

---

### 0.4 Imprimer le panier

**Options d'impression :**

#### A) Imprimante personnelle
- Creality Ender 3 (200-300€)
- Prusa i3 MK3S+ (700-1000€)
- Anycubic i3 Mega (150-250€)

#### B) Service d'impression 3D local
- FabLab : https://www.fablabfinder.org
- Localisez le plus proche de chez vous
- Coût : 5-20€ selon la taille

#### C) Service en ligne
- 3DHubs : https://www.3dhubs.com
- Craftcloud : https://craftcloud3d.com
- Sculpteo : https://www.sculpteo.com
- Coût : 15-50€ + frais de port

**Après impression :**
1. Laisser refroidir complètement (30 min)
2. Retirer du plateau (outil à spatule)
3. Enlever les supports (lame fine)
4. Poncer légèrement (grain 220)
5. Nettoyer avec un chiffon humide

---

### 0.5 Intégrer les antennes RFID

**Préparation des antennes :**

#### Type 1 : Antennes commerciales RFID
```
- Diamètre : 80mm
- Fréquence : 125kHz ou 13.56MHz
- Gain : 2-3 dBi
- Coût : 20-50€ par antenne
- Fournisseurs : AliExpress, Amazon, Digikey
```

#### Type 2 : Fabriquer les antennes
**Matériel :**
- Câble coaxial RG58 (5€)
- Connecteurs SMA (2€)
- Multimètre

**Formule pour bobiner une antenne RFID :**
```
Pour 125kHz (basse fréquence) :
- Nombre de spires : 5-7
- Diamètre de la bobine : 80mm
- Fil de cuivre : 0.8-1mm
```

**Installation dans le panier :**

```
Vue de dessus du panier :
┌─────────────────────────────┐
│ Antenne 1    │    Antenne 2 │
│    (coin)    │    (coin)    │
│              │              │
│              │              │
│    Antenne 3 │    Antenne 4 │
│    (coin)    │    (coin)    │
└─────────────────────────────┘

Montage :
1. Fixer les antennes avec adhésif double-face (TM04 3M)
2. Positionner au centre des emplacements réservés
3. Laisser 5mm d'épaisseur pour le câblage
4. Câbler les antennes en parallèle vers le lecteur
```

---

### 0.6 Câblage du panier

**Schéma de connexion :**

```
Lecteur RFID USB
      │
      └─── Câble USB vers PC
      
Antennes dans le panier
      │
      ├─ Antenne 1 (80mm)
      ├─ Antenne 2 (80mm)
      ├─ Antenne 3 (80mm)
      └─ Antenne 4 (80mm)
      
      └─── Câble coaxial (RG58)
            └─ Vers connecteur SMA du lecteur
```

**Connexion détaillée :**

1. **Lecteur RFID vers PC :**
   - Câble USB-A vers USB Mini/Micro
   - Port USB 2.0 ou 3.0
   - Alimentation : directement par USB

2. **Antennes vers Lecteur :**
   - Configuration : Antennes en parallèle
   - Impédance : 50 Ohms
   - Longueur de câble : max 3m recommandé

3. **Écran vers PC :**
   - HDMI (si disponible)
   - Ou USB (écrans tactiles USB)
   - Alimentation : USB ou adaptateur 5V

---

### 0.7 Tester le matériel

**Test du lecteur RFID :**

```powershell
# Installer pyserial pour la communication série
pip install pyserial

# Créer un script de test
```

**Créez le fichier :** `test_rfid_hardware.py`

```python
import serial
import time

# Configuration du port série
# Pour trouver le port COM : 
#   Gestionnaire des périphériques → Ports (COM et LPT)

PORT = "COM3"  # À adapter selon votre système
BAUDRATE = 9600  # À vérifier selon le lecteur

def tester_lecteur_rfid():
    """Tester la connexion avec le lecteur RFID"""
    
    try:
        ser = serial.Serial(PORT, BAUDRATE, timeout=1)
        print(f"✅ Lecteur RFID connecté sur {PORT}")
        
        print("\n📡 En attente de scan RFID...")
        print("Approchez une étiquette RFID du lecteur...\n")
        
        while True:
            if ser.in_waiting:
                # Lire les données du lecteur
                raw_data = ser.readline()
                code_rfid = raw_data.decode('utf-8').strip()
                
                if code_rfid:
                    print(f"✅ Code RFID scanné : {code_rfid}")
                    print(f"   Longueur : {len(code_rfid)} caractères")
                    print(f"   Format hexadécimal : {code_rfid.encode('utf-8').hex()}\n")
            
            time.sleep(0.1)
    
    except serial.SerialException as e:
        print(f"❌ Erreur de connexion : {e}")
        print(f"\nPorts COM disponibles :")
        print("   - Allez dans Gestionnaire des périphériques")
        print("   - Ports (COM et LPT)")
        print("   - Notez les numéros de port (COM1, COM2, etc.)")
    
    except KeyboardInterrupt:
        print("\n\n👋 Test terminé")
        ser.close()

if __name__ == "__main__":
    tester_lecteur_rfid()
```

**Comment exécuter :**
```powershell
python test_rfid_hardware.py
```

**Résultat attendu :**
```
✅ Lecteur RFID connecté sur COM3
📡 En attente de scan RFID...
Approchez une étiquette RFID du lecteur...

✅ Code RFID scanné : 0000AB12CD
```

---

### 0.8 Vérifier la qualité de détection

**Test de portée :**

```
Distance de détection recommandée :
- RFID 125kHz : 0-10cm (selon antenne)
- RFID 13.56MHz : 0-5cm

Test :
1. Placez l'étiquette à 1cm du lecteur → ✅ Détectée
2. Placez à 5cm → ✅ Détectée
3. Placez à 10cm → À voir selon le lecteur
4. Distance maximale : notez-la pour le panier
```

**Test de couverture du panier :**

```
┌─────────────────────────────┐
│ Antenne 1    │    Antenne 2 │
│     ✓        │      ✓       │  → Points de détection
│              │              │
│     ✓        │      ✓       │
│ Antenne 3    │    Antenne 4 │
└─────────────────────────────┘

Placer des étiquettes RFID à différents endroits du panier
et vérifier qu'elles sont toutes détectées.
```

         ↑─────────────────────────────┘
         │ Lecture RFID réelle
         │ (lecteur USB RFID physique)
```

### Objectif
Installer tous les outils nécessaires pour développer le projet.

### 1.1 Vérifier que Python est installé

**Pourquoi ?** Python est le langage principal du projet.

**Comment faire :**
1. Ouvrez **PowerShell** (clic droit sur Bureau → PowerShell)
2. Tapez la commande :
```powershell
python --version
```
3. Vous devriez voir : `Python 3.x.x`

**Si ça ne marche pas :**
- Allez sur https://www.python.org/
- Téléchargez Python 3.11+
- **IMPORTANT** : Cochez "Add Python to PATH" pendant l'installation
- Redémarrez PowerShell
- Réessayez

---

### 1.2 Créer un dossier pour le projet

**Pourquoi ?** Pour organiser tous les fichiers du projet.

**Comment faire :**
1. Ouvrez PowerShell
2. Exécutez :
```powershell
cd "C:\Users\SARA\Desktop\Panier intelligent"
mkdir AutomaticCheck_Dev
cd AutomaticCheck_Dev
```

---

### 1.3 Créer un environnement virtuel Python

**Pourquoi ?** Cela isole les installations de ce projet des autres projects.

**Comment faire :**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Résultat attendu :** Vous verrez `(venv)` au début de chaque ligne PowerShell

---

### 1.4 Installer les bibliothèques nécessaires

**Pourquoi ?** Ces bibliothèques nous donnent les outils pour créer l'application.

**Comment faire :**
```powershell
pip install fastapi uvicorn pyqt6 sqlalchemy sqlite3 python-dateutil
```

**Explication de chaque librairie :**
- **fastapi** : Crée le serveur backend
- **uvicorn** : Lance le serveur
- **pyqt6** : Crée l'interface graphique
- **sqlalchemy** : Gère la base de données
- **python-dateutil** : Gère les dates

**Durée :** 2-3 minutes

---

### 1.5 Vérifier l'installation

**Comment faire :**
```powershell
pip list
```

Vous devriez voir les packages listés.

---

## 💾 ÉTAPE 2 : Mise en place de la base de données {#étape-2}

### Objectif
Créer la base de données SQLite avec toutes les tables nécessaires.

### 2.1 Créer le fichier de configuration de la BD

**Créez le fichier :** `database.py`

**Contenu :**
```python
import sqlite3
from pathlib import Path

# Chemin de la base de données
DB_PATH = Path(__file__).parent / "automaticcheck.db"

def init_database():
    """Initialiser la base de données avec les tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Table des produits
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            prix REAL NOT NULL,
            stock INTEGER NOT NULL DEFAULT 100,
            code_rfid TEXT UNIQUE NOT NULL,
            categorie TEXT DEFAULT 'Général',
            date_ajout TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Table des factures
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS factures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date_heure TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total REAL NOT NULL,
            nombre_articles INTEGER NOT NULL,
            statut TEXT DEFAULT 'En cours'
        )
    """)
    
    # Table des articles dans les factures
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS articles_facture (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facture_id INTEGER NOT NULL,
            produit_id INTEGER NOT NULL,
            quantite INTEGER NOT NULL,
            prix_unitaire REAL NOT NULL,
            FOREIGN KEY (facture_id) REFERENCES factures(id),
            FOREIGN KEY (produit_id) REFERENCES produits(id)
        )
    """)
    
    # Table des paiements
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS paiements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            facture_id INTEGER NOT NULL,
            mode_paiement TEXT NOT NULL,
            montant REAL NOT NULL,
            date_heure TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            statut TEXT DEFAULT 'Accepté',
            FOREIGN KEY (facture_id) REFERENCES factures(id)
        )
    """)
    
    conn.commit()
    conn.close()
    print("✅ Base de données initialisée avec succès !")

def ajouter_produits_demo():
    """Ajouter des produits de test"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    produits_demo = [
        ("Pain", 1.50, 50, "RFID001", "Boulangerie"),
        ("Lait", 2.00, 40, "RFID002", "Laiterie"),
        ("Fromage", 5.00, 30, "RFID003", "Laiterie"),
        ("Tomate", 1.20, 60, "RFID004", "Fruits/Légumes"),
        ("Pomme", 0.80, 100, "RFID005", "Fruits/Légumes"),
        ("Chocolat", 2.50, 45, "RFID006", "Confiserie"),
        ("Eau 1L", 1.00, 80, "RFID007", "Boissons"),
        ("Café", 4.50, 25, "RFID008", "Boissons"),
    ]
    
    for nom, prix, stock, code_rfid, categorie in produits_demo:
        try:
            cursor.execute("""
                INSERT INTO produits (nom, prix, stock, code_rfid, categorie)
                VALUES (?, ?, ?, ?, ?)
            """, (nom, prix, stock, code_rfid, categorie))
        except sqlite3.IntegrityError:
            print(f"⚠️ Produit {nom} déjà existant")
    
    conn.commit()
    conn.close()
    print("✅ Produits de démonstration ajoutés !")

if __name__ == "__main__":
    init_database()
    ajouter_produits_demo()
```

**Comment exécuter :**
```powershell
python database.py
```

**Résultat attendu :** Vous verrez les messages ✅

---

### 2.2 Vérifier la base de données

**Comment faire :**
1. Téléchargez **DB Browser for SQLite** : https://sqlitebrowser.org/
2. Ouvrez `automaticcheck.db` avec cet outil
3. Vous verrez toutes les tables et les produits créés

---

## 🔧 ÉTAPE 3 : Développement du backend {#étape-3}

### Objectif
Créer le serveur qui gère :
- Les produits
- Les factures
- Les paiements
- Les stocks

### 3.1 Créer le fichier backend

**Créez le fichier :** `backend.py`

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import sqlite3
from pathlib import Path
from datetime import datetime
from pydantic import BaseModel
from typing import List

app = FastAPI(title="AutomaticCheck Backend")

DB_PATH = Path(__file__).parent / "automaticcheck.db"

# ============= MODÈLES DE DONNÉES =============

class Produit(BaseModel):
    id: int
    nom: str
    prix: float
    stock: int
    code_rfid: str
    categorie: str

class ArticleFacture(BaseModel):
    produit_id: int
    quantite: int = 1

class Facture(BaseModel):
    articles: List[ArticleFacture]
    mode_paiement: str

class Paiement(BaseModel):
    montant: float
    mode_paiement: str

# ============= FONCTION UTILITAIRE =============

def get_db():
    """Connexion à la base de données"""
    return sqlite3.connect(DB_PATH)

# ============= ROUTES : PRODUITS =============

@app.get("/api/produits", response_model=List[Produit])
def lister_produits():
    """Lister tous les produits disponibles"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nom, prix, stock, code_rfid, categorie FROM produits")
    produits = cursor.fetchall()
    conn.close()
    
    return [
        Produit(
            id=p[0],
            nom=p[1],
            prix=p[2],
            stock=p[3],
            code_rfid=p[4],
            categorie=p[5]
        )
        for p in produits
    ]

@app.get("/api/produits/{code_rfid}")
def obtenir_produit_par_rfid(code_rfid: str):
    """Obtenir un produit par son code RFID"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nom, prix, stock, code_rfid, categorie 
        FROM produits 
        WHERE code_rfid = ?
    """, (code_rfid,))
    
    produit = cursor.fetchone()
    conn.close()
    
    if not produit:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    
    return {
        "id": produit[0],
        "nom": produit[1],
        "prix": produit[2],
        "stock": produit[3],
        "code_rfid": produit[4],
        "categorie": produit[5]
    }

# ============= ROUTES : FACTURES =============

@app.post("/api/factures")
def creer_facture(facture_data: Facture):
    """Créer une facture avec les articles scannés"""
    
    if not facture_data.articles:
        raise HTTPException(status_code=400, detail="Aucun article dans la facture")
    
    conn = get_db()
    cursor = conn.cursor()
    
    total = 0
    articles_details = []
    
    # Calculer le total et vérifier les stocks
    for article in facture_data.articles:
        cursor.execute(
            "SELECT nom, prix, stock FROM produits WHERE id = ?",
            (article.produit_id,)
        )
        produit = cursor.fetchone()
        
        if not produit:
            conn.close()
            raise HTTPException(status_code=404, detail=f"Produit {article.produit_id} non trouvé")
        
        if produit[2] < article.quantite:
            conn.close()
            raise HTTPException(
                status_code=400,
                detail=f"Stock insuffisant pour {produit[0]}"
            )
        
        prix_total_article = produit[1] * article.quantite
        total += prix_total_article
        articles_details.append({
            "produit_id": article.produit_id,
            "nom": produit[0],
            "prix_unitaire": produit[1],
            "quantite": article.quantite,
            "total": prix_total_article
        })
    
    # Créer la facture
    cursor.execute("""
        INSERT INTO factures (total, nombre_articles, statut)
        VALUES (?, ?, ?)
    """, (total, len(facture_data.articles), "En cours"))
    
    facture_id = cursor.lastrowid
    
    # Ajouter les articles
    for article in articles_details:
        cursor.execute("""
            INSERT INTO articles_facture (facture_id, produit_id, quantite, prix_unitaire)
            VALUES (?, ?, ?, ?)
        """, (facture_id, article["produit_id"], article["quantite"], article["prix_unitaire"]))
        
        # Mettre à jour le stock
        cursor.execute(
            "UPDATE produits SET stock = stock - ? WHERE id = ?",
            (article["quantite"], article["produit_id"])
        )
    
    conn.commit()
    conn.close()
    
    return {
        "facture_id": facture_id,
        "total": total,
        "articles": articles_details,
        "mode_paiement": facture_data.mode_paiement
    }

@app.get("/api/factures/{facture_id}")
def obtenir_facture(facture_id: int):
    """Obtenir les détails d'une facture"""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT id, date_heure, total, nombre_articles, statut FROM factures WHERE id = ?",
        (facture_id,)
    )
    facture = cursor.fetchone()
    
    if not facture:
        conn.close()
        raise HTTPException(status_code=404, detail="Facture non trouvée")
    
    cursor.execute("""
        SELECT af.quantite, af.prix_unitaire, p.nom
        FROM articles_facture af
        JOIN produits p ON af.produit_id = p.id
        WHERE af.facture_id = ?
    """, (facture_id,))
    
    articles = cursor.fetchall()
    conn.close()
    
    return {
        "id": facture[0],
        "date": facture[1],
        "total": facture[2],
        "nombre_articles": facture[3],
        "statut": facture[4],
        "articles": [{"nom": a[2], "quantite": a[0], "prix": a[1]} for a in articles]
    }

# ============= ROUTES : PAIEMENTS =============

@app.post("/api/paiements/{facture_id}")
def enregistrer_paiement(facture_id: int, paiement: Paiement):
    """Enregistrer un paiement pour une facture"""
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Vérifier que la facture existe
    cursor.execute("SELECT total FROM factures WHERE id = ?", (facture_id,))
    facture = cursor.fetchone()
    
    if not facture:
        conn.close()
        raise HTTPException(status_code=404, detail="Facture non trouvée")
    
    # Enregistrer le paiement
    cursor.execute("""
        INSERT INTO paiements (facture_id, mode_paiement, montant, statut)
        VALUES (?, ?, ?, ?)
    """, (facture_id, paiement.mode_paiement, paiement.montant, "Accepté"))
    
    # Mettre à jour le statut de la facture
    cursor.execute(
        "UPDATE factures SET statut = ? WHERE id = ?",
        ("Payée", facture_id)
    )
    
    conn.commit()
    conn.close()
    
    return {
        "message": "Paiement enregistré avec succès",
        "facture_id": facture_id,
        "montant": paiement.montant,
        "mode": paiement.mode_paiement
    }

# ============= ROUTE SANTÉ =============

@app.get("/api/health")
def health_check():
    """Vérifier que le serveur fonctionne"""
    return {"status": "✅ Le serveur fonctionne !"}

# ============= LANCEMENT =============

if __name__ == "__main__":
    import uvicorn
    print("🚀 Démarrage du serveur AutomaticCheck...")
    print("📍 URL : http://localhost:8000")
    print("📚 Documentation : http://localhost:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

**Comment exécuter :**
```powershell
python backend.py
```

**Résultat attendu :**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Tester le serveur :**
Ouvrez dans votre navigateur : http://localhost:8000/docs

---

## 🎨 ÉTAPE 4 : Développement du frontend {#étape-4}

### Objectif
Créer l'interface graphique que l'utilisateur voit.

### 4.1 Créer l'interface principale

**Créez le fichier :** `frontend.py`

```python
import sys
import requests
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QListWidget, QListWidgetItem, QLineEdit,
    QComboBox, QMessageBox, QTableWidget, QTableWidgetItem, QTabWidget
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont, QColor
from datetime import datetime

API_URL = "http://localhost:8000/api"

class AutomaticCheckApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🛒 AutomaticCheck - Borne de Caisse Automatique")
        self.setGeometry(100, 100, 1200, 800)
        
        # Variables
        self.panier = []  # Liste des articles du panier
        self.facture_actuelle = None
        
        # Initialiser l'interface
        self.init_ui()
        
        # Charger les produits au démarrage
        self.charger_produits()
    
    def init_ui(self):
        """Initialiser l'interface utilisateur"""
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        layout_principal = QHBoxLayout()
        
        # ========== PANNEAU GAUCHE : Produits ==========
        layout_gauche = QVBoxLayout()
        
        label_produits = QLabel("📦 PRODUITS DISPONIBLES")
        label_produits.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout_gauche.addWidget(label_produits)
        
        # Liste des produits
        self.liste_produits = QListWidget()
        self.liste_produits.itemClicked.connect(self.selectionner_produit)
        layout_gauche.addWidget(self.liste_produits)
        
        # Bouton pour scanner/ajouter
        btn_ajouter = QPushButton("➕ Ajouter au panier")
        btn_ajouter.clicked.connect(self.ajouter_au_panier)
        btn_ajouter.setStyleSheet("background-color: #4CAF50; color: white; font-size: 12px; padding: 10px;")
        layout_gauche.addWidget(btn_ajouter)
        
        # ========== PANNEAU CENTRE : Panier ==========
        layout_centre = QVBoxLayout()
        
        label_panier = QLabel("🛍️ VOTRE PANIER")
        label_panier.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout_centre.addWidget(label_panier)
        
        # Tableau du panier
        self.tableau_panier = QTableWidget()
        self.tableau_panier.setColumnCount(5)
        self.tableau_panier.setHorizontalHeaderLabels(["Article", "Prix", "Quantité", "Total", "Supprimer"])
        layout_centre.addWidget(self.tableau_panier)
        
        # Total
        self.label_total = QLabel("💰 TOTAL : 0.00 €")
        self.label_total.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.label_total.setStyleSheet("background-color: #FFD700; padding: 10px; border-radius: 5px;")
        layout_centre.addWidget(self.label_total)
        
        # ========== PANNEAU DROIT : Paiement ==========
        layout_droit = QVBoxLayout()
        
        label_paiement = QLabel("💳 PAIEMENT")
        label_paiement.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        layout_droit.addWidget(label_paiement)
        
        # Mode de paiement
        label_mode = QLabel("Choisir le mode de paiement :")
        layout_droit.addWidget(label_mode)
        
        self.combo_paiement = QComboBox()
        self.combo_paiement.addItems(["Liquide", "Carte bancaire", "Mobile Money"])
        layout_droit.addWidget(self.combo_paiement)
        
        # Espace
        layout_droit.addSpacing(20)
        
        # Affichage de la facture
        label_facture = QLabel("📄 FACTURE")
        label_facture.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        layout_droit.addWidget(label_facture)
        
        self.label_facture = QLabel("")
        self.label_facture.setFont(QFont("Courier", 10))
        self.label_facture.setStyleSheet("background-color: #f0f0f0; padding: 10px; border: 1px solid #ccc;")
        layout_droit.addWidget(self.label_facture)
        
        layout_droit.addSpacing(20)
        
        # Boutons d'action
        btn_valider = QPushButton("✅ VALIDER ET PAYER")
        btn_valider.clicked.connect(self.valider_paiement)
        btn_valider.setStyleSheet("background-color: #2196F3; color: white; font-size: 12px; padding: 15px; font-weight: bold;")
        layout_droit.addWidget(btn_valider)
        
        btn_annuler = QPushButton("❌ ANNULER")
        btn_annuler.clicked.connect(self.annuler_panier)
        btn_annuler.setStyleSheet("background-color: #f44336; color: white; font-size: 12px; padding: 15px;")
        layout_droit.addWidget(btn_annuler)
        
        # Assemler les layouts
        layout_principal.addLayout(layout_gauche, 1)
        layout_principal.addLayout(layout_centre, 1)
        layout_principal.addLayout(layout_droit, 1)
        
        central_widget.setLayout(layout_principal)
    
    def charger_produits(self):
        """Charger la liste des produits depuis l'API"""
        try:
            response = requests.get(f"{API_URL}/produits")
            if response.status_code == 200:
                produits = response.json()
                self.liste_produits.clear()
                
                for produit in produits:
                    # Créer un item avec les informations du produit
                    texte = f"{produit['nom']} - {produit['prix']}€ (Stock: {produit['stock']})"
                    item = QListWidgetItem(texte)
                    item.setData(Qt.ItemDataRole.UserRole, produit['id'])
                    item.setData(Qt.ItemDataRole.UserRole + 1, produit['code_rfid'])
                    self.liste_produits.addItem(item)
        except requests.exceptions.ConnectionError:
            QMessageBox.critical(self, "Erreur", "❌ Impossible de se connecter au serveur!\nAssurez-vous que le backend est lancé.")
    
    def selectionner_produit(self, item):
        """Sélectionner un produit de la liste"""
        self.produit_selectionne = {
            'id': item.data(Qt.ItemDataRole.UserRole),
            'rfid': item.data(Qt.ItemDataRole.UserRole + 1)
        }
    
    def ajouter_au_panier(self):
        """Ajouter le produit sélectionné au panier"""
        if not hasattr(self, 'produit_selectionne'):
            QMessageBox.warning(self, "Attention", "⚠️ Veuillez sélectionner un produit !")
            return
        
        # Récupérer les infos du produit
        try:
            response = requests.get(f"{API_URL}/produits/{self.produit_selectionne['rfid']}")
            produit = response.json()
            
            # Ajouter au panier
            self.panier.append(produit)
            self.mettre_a_jour_affichage()
            
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"❌ Erreur : {str(e)}")
    
    def mettre_a_jour_affichage(self):
        """Mettre à jour l'affichage du panier et du total"""
        
        # Vider le tableau
        self.tableau_panier.setRowCount(0)
        
        total = 0
        
        # Compter les occurrences
        compteur = {}
        for produit in self.panier:
            produit_id = produit['id']
            if produit_id not in compteur:
                compteur[produit_id] = {
                    'produit': produit,
                    'quantite': 0
                }
            compteur[produit_id]['quantite'] += 1
        
        # Afficher dans le tableau
        row = 0
        for produit_id, data in compteur.items():
            produit = data['produit']
            quantite = data['quantite']
            total_article = produit['prix'] * quantite
            total += total_article
            
            # Ajouter une ligne
            self.tableau_panier.insertRow(row)
            
            self.tableau_panier.setItem(row, 0, QTableWidgetItem(produit['nom']))
            self.tableau_panier.setItem(row, 1, QTableWidgetItem(f"{produit['prix']:.2f}€"))
            self.tableau_panier.setItem(row, 2, QTableWidgetItem(str(quantite)))
            self.tableau_panier.setItem(row, 3, QTableWidgetItem(f"{total_article:.2f}€"))
            
            btn_supprimer = QPushButton("🗑️")
            btn_supprimer.clicked.connect(lambda checked, p_id=produit_id: self.supprimer_du_panier(p_id))
            self.tableau_panier.setCellWidget(row, 4, btn_supprimer)
            
            row += 1
        
        # Mettre à jour le total
        self.label_total.setText(f"💰 TOTAL : {total:.2f}€")
        
        # Générer la facture
        self.generer_facture(total)
    
    def generer_facture(self, total):
        """Générer le texte de la facture"""
        facture_text = f"""
╔════════════════════════════════╗
║    FACTURE AUTOMATICCHECK      ║
╚════════════════════════════════╝

Date: {datetime.now().strftime('%d/%m/%Y %H:%M')}

─────────────────────────────────
ARTICLES:
"""
        
        compteur = {}
        for produit in self.panier:
            if produit['id'] not in compteur:
                compteur[produit['id']] = {
                    'nom': produit['nom'],
                    'prix': produit['prix'],
                    'quantite': 0
                }
            compteur[produit['id']]['quantite'] += 1
        
        for data in compteur.values():
            sous_total = data['prix'] * data['quantite']
            facture_text += f"\n{data['nom']:<20} x{data['quantite']:>2} = {sous_total:>7.2f}€"
        
        facture_text += f"""

─────────────────────────────────
TOTAL: {total:.2f}€
─────────────────────────────────
Mode de paiement: {self.combo_paiement.currentText()}

Merci pour votre achat ! 🎉
"""
        
        self.label_facture.setText(facture_text)
    
    def supprimer_du_panier(self, produit_id):
        """Supprimer un produit du panier"""
        self.panier = [p for p in self.panier if p['id'] != produit_id]
        self.mettre_a_jour_affichage()
    
    def valider_paiement(self):
        """Valider la commande et enregistrer le paiement"""
        
        if not self.panier:
            QMessageBox.warning(self, "Attention", "⚠️ Le panier est vide !")
            return
        
        # Préparer les données pour créer la facture
        articles = []
        compteur = {}
        
        for produit in self.panier:
            if produit['id'] not in compteur:
                compteur[produit['id']] = 0
            compteur[produit['id']] += 1
        
        for produit_id, quantite in compteur.items():
            articles.append({
                "produit_id": produit_id,
                "quantite": quantite
            })
        
        data = {
            "articles": articles,
            "mode_paiement": self.combo_paiement.currentText()
        }
        
        try:
            # Créer la facture
            response = requests.post(f"{API_URL}/factures", json=data)
            facture = response.json()
            
            # Enregistrer le paiement
            paiement_data = {
                "montant": facture['total'],
                "mode_paiement": self.combo_paiement.currentText()
            }
            
            requests.post(
                f"{API_URL}/paiements/{facture['facture_id']}",
                json=paiement_data
            )
            
            # Afficher le succès
            QMessageBox.information(
                self,
                "✅ Paiement réussi !",
                f"Facture n°{facture['facture_id']}\nTotal: {facture['total']:.2f}€\n\nMerci pour votre achat !"
            )
            
            # Réinitialiser
            self.annuler_panier()
            
        except Exception as e:
            QMessageBox.critical(self, "❌ Erreur", f"Erreur lors du paiement: {str(e)}")
    
    def annuler_panier(self):
        """Annuler et réinitialiser le panier"""
        self.panier = []
        self.tableau_panier.setRowCount(0)
        self.label_total.setText("💰 TOTAL : 0.00€")
        self.label_facture.setText("")


def main():
    app = QApplication(sys.argv)
    window = AutomaticCheckApp()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
```

**Comment exécuter :**

Dans un autre PowerShell (en gardant le backend lancé) :
```powershell
cd "C:\Users\SARA\Desktop\Panier intelligent\AutomaticCheck_Dev"
.\venv\Scripts\Activate.ps1
python frontend.py
```

---

## 📡 ÉTAPE 5 : Intégration RFID réelle {#étape-5}

### Objectif
Connecter le vrai lecteur RFID et lire les codes physiques des produits.

### 5.1 Identifier votre lecteur RFID

**Modèles recommandés :**

#### Option 1 : Lecteur USB 125kHz (Bas coût, excellent)
- Modèle : ID Innovations ID20/ID25 USB
- Prix : 20-40€
- Format : Clavier USB (clé RFID apparaît comme du texte tapé)
- Avantage : Très facile à intégrer
- Lien : AliExpress, Amazon

#### Option 2 : Lecteur 13.56MHz
- Modèle : Lecteur HF RFID 13.56MHz USB
- Prix : 30-50€
- Format : Communique via port série
- Avantage : Portée plus grande

#### Option 3 : Module Arduino RC522
- Prix : 5-10€
- Nécessite : Arduino/Raspberry Pi
- Plus complexe mais très flexibile

**Pour cette feuille de route, on suppose un lecteur USB 125kHz (plus simple).**

---

### 5.2 Connecter le lecteur RFID

**Étapes :**

1. **Brancher le lecteur USB**
   - Connecter au port USB de votre ordinateur
   - Windows devrait le reconnaître automatiquement
   - Pas de driver nécessaire généralement

2. **Vérifier la connexion**
   - Aller dans Gestionnaire des périphériques
   - Contrôler que le lecteur apparaît

3. **Tester manuellement**
   - Ouvrir le Bloc-notes
   - Placer une étiquette RFID devant le lecteur
   - Le code doit s'afficher automatiquement

---

### 5.3 Créer le module RFID réel

**Créez le fichier :** `rfid_reader.py`

```python
import serial
import threading
import time
from queue import Queue
from typing import Callable

class RFIDReader:
    """Lecteur RFID réel via port série USB"""
    
    def __init__(self, port: str = None, baudrate: int = 9600):
        """
        Initialiser le lecteur RFID
        
        Args:
            port : Port COM (ex: "COM3"). Si None, détecte automatiquement.
            baudrate : Vitesse série (défaut: 9600)
        """
        self.port = port
        self.baudrate = baudrate
        self.serial = None
        self.running = False
        self.thread = None
        self.callback_queue = Queue()
        self.scan_callback = None
        
    def trouver_port_com(self):
        """Trouver le port COM du lecteur RFID"""
        import serial.tools.list_ports
        
        ports = serial.tools.list_ports.comports()
        
        if not ports:
            raise Exception("❌ Aucun port série trouvé")
        
        print(f"Ports COM disponibles :")
        for i, (port, desc, hwid) in enumerate(ports):
            print(f"  {i+1}. {port} - {desc}")
        
        # Sélectionner le premier port (généralement le lecteur RFID)
        return ports[0][0]
    
    def connecter(self):
        """Connecter au lecteur RFID"""
        try:
            if not self.port:
                self.port = self.trouver_port_com()
            
            self.serial = serial.Serial(
                self.port,
                self.baudrate,
                timeout=1
            )
            print(f"✅ Lecteur RFID connecté sur {self.port}")
            
            # Démarrer le thread de lecture
            self.running = True
            self.thread = threading.Thread(target=self._lire_boucle, daemon=True)
            self.thread.start()
            
        except Exception as e:
            print(f"❌ Erreur de connexion : {e}")
            raise
    
    def _lire_boucle(self):
        """Boucle de lecture des codes RFID"""
        while self.running:
            try:
                if self.serial and self.serial.in_waiting:
                    # Lire une ligne
                    raw_data = self.serial.readline()
                    code_rfid = raw_data.decode('utf-8').strip()
                    
                    if code_rfid:
                        print(f"📡 Code RFID scanné : {code_rfid}")
                        
                        # Ajouter à la queue
                        self.callback_queue.put(code_rfid)
                        
                        # Appeler le callback si défini
                        if self.scan_callback:
                            self.scan_callback(code_rfid)
                
                time.sleep(0.05)
            
            except Exception as e:
                print(f"⚠️ Erreur lecture : {e}")
    
    def obtenir_code(self, timeout=5):
        """
        Obtenir le prochain code RFID scanné
        
        Args:
            timeout : Temps maximum d'attente en secondes
        
        Returns:
            Code RFID ou None si timeout
        """
        try:
            return self.callback_queue.get(timeout=timeout)
        except:
            return None
    
    def definir_callback(self, callback: Callable):
        """
        Définir une fonction à appeler quand un code est scanné
        
        Args:
            callback : Fonction(code_rfid) appelée à chaque scan
        """
        self.scan_callback = callback
    
    def deconnecter(self):
        """Déconnecter le lecteur"""
        self.running = False
        if self.thread:
            self.thread.join(timeout=1)
        if self.serial:
            self.serial.close()
        print("👋 Lecteur RFID déconnecté")


# Test
if __name__ == "__main__":
    try:
        reader = RFIDReader()
        reader.connecter()
        
        print("\n📡 En attente de scans RFID...")
        print("Approchez les étiquettes du lecteur...\n")
        
        # Boucle de test
        for i in range(10):  # Lire 10 codes max
            code = reader.obtenir_code(timeout=10)
            if code:
                print(f"✅ Reçu : {code}")
            else:
                print("⏱️ Timeout")
        
        reader.deconnecter()
    
    except Exception as e:
        print(f"Erreur : {e}")
```

**Test du lecteur :**
```powershell
python rfid_reader.py
```

---

### 5.4 Intégrer RFID dans le backend

**Modifier `backend.py` pour ajouter :**

```python
# Ajouter à la fin du fichier backend.py, AVANT la section de lancement

from rfid_reader import RFIDReader
import threading

# Créer une instance globale du lecteur RFID
rfid_reader = None

def initialiser_rfid():
    """Initialiser le lecteur RFID"""
    global rfid_reader
    try:
        rfid_reader = RFIDReader()
        rfid_reader.connecter()
        print("✅ Lecteur RFID initialisé")
    except Exception as e:
        print(f"⚠️ Avertissement : Lecteur RFID non disponible ({e})")
        print("   Vous pouvez continuer sans lecteur RFID")

# Démarrer le lecteur RFID avant le serveur
if __name__ == "__main__":
    import uvicorn
    
    # Initialiser le lecteur RFID dans un thread séparé
    thread_rfid = threading.Thread(target=initialiser_rfid, daemon=True)
    thread_rfid.start()
    
    time.sleep(1)  # Laisser le temps au lecteur de se connecter
    
    print("🚀 Démarrage du serveur AutomaticCheck...")
    print("📍 URL : http://localhost:8000")
    print("📚 Documentation : http://localhost:8000/docs")
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

---

### 5.5 Intégrer RFID dans le frontend

**Modifier `frontend.py` pour ajouter une lecture RFID en temps réel :**

```python
import threading
import requests

# Ajouter cette fonction dans la classe AutomaticCheckApp

def lancer_lecteur_rfid_background(self):
    """Lancer la lecture RFID en arrière-plan"""
    def lire_rfid():
        try:
            from rfid_reader import RFIDReader
            
            reader = RFIDReader()
            reader.connecter()
            
            print("✅ Lecteur RFID prêt")
            
            while True:
                code = reader.obtenir_code(timeout=None)
                if code:
                    # Chercher le produit avec ce code RFID
                    try:
                        response = requests.get(f"{API_URL}/produits/{code}")
                        if response.status_code == 200:
                            produit = response.json()
                            self.panier.append(produit)
                            # Mettre à jour l'interface dans le thread principal
                            self.mettre_a_jour_affichage()
                    except:
                        pass
        
        except Exception as e:
            print(f"Lecteur RFID : {e}")
    
    # Lancer le lecteur dans un thread séparé
    thread = threading.Thread(target=lire_rfid, daemon=True)
    thread.start()

# Dans __init__, ajouter après self.init_ui() :
# self.lancer_lecteur_rfid_background()
```

---

### 5.6 Étiqueter les produits avec RFID

**Préparation des étiquettes :**

1. **Acheter des étiquettes RFID**
   - Format : Adhésifs, plastique, papier
   - Fréquence : Doit correspondre à votre lecteur (125kHz ou 13.56MHz)
   - Prix : 0.5-2€ par étiquette
   - Quantité : Au minimum 8 (un par produit de démo)

2. **Programmer les étiquettes**
   - Utiliser un programmeur RFID (30-100€)
   - Ou service en ligne (certains fournisseurs programment)
   - Codes à programmer : RFID001 à RFID008

3. **Coller les étiquettes**
   - Une étiquette par produit (ou boîte de produit)
   - Placer de manière accessible pour le lecteur

---

### 5.7 Schéma de câblage complet

```
ORDINATEUR
├─ Port USB 1 → Lecteur RFID USB
│              └─ Détecte automatiquement
│
├─ Port USB 2 → Écran HDMI (via adaptateur USB)
│
└─ Port USB 3 → (disponible pour expansion)

PANIER (Boîte physique)
├─ Antenne 1 (coin haut-gauche)
├─ Antenne 2 (coin haut-droit)
├─ Antenne 3 (coin bas-gauche)
└─ Antenne 4 (coin bas-droit)
   └─ Câble coaxial vers lecteur RFID

PROCESSUS DE SCAN
1. Client dépose produit dans le panier
2. Antennes RFID du panier scanent l'étiquette
3. Code RFID transmis au lecteur USB
4. PC reçoit le code via USB
5. Backend recherche le produit
6. Frontend affiche le produit et met à jour le panier
```

---

## 🧪 ÉTAPE 6 : Tests et validation {#étape-6}

### Objectif
Tester toutes les fonctionnalités de l'application.

### 6.1 Checklist de test

```
[ ] Base de données créée
    - [ ] Table produits
    - [ ] Table factures
    - [ ] Table articles_facture
    - [ ] Table paiements

[ ] Backend fonctionne
    - [ ] http://localhost:8000/docs accessible
    - [ ] GET /api/produits retourne les produits
    - [ ] GET /api/produits/{code_rfid} retourne un produit
    - [ ] POST /api/factures crée une facture

[ ] Frontend fonctionne
    - [ ] Affichage des produits
    - [ ] Ajout au panier
    - [ ] Calcul du total
    - [ ] Génération facture

[ ] Paiement
    - [ ] Sélection du mode de paiement
    - [ ] Enregistrement du paiement
    - [ ] Message de confirmation

[ ] RFID
    - [ ] Scan manuel du clavier
    - [ ] Code RFID valide = produit ajouté
    - [ ] Code RFID invalide = message d'erreur

[ ] Stocks
    - [ ] Stock diminue après achat
    - [ ] Impossible d'acheter plus que le stock
```

### 6.2 Tests manuels

**Test 1 : Ajouter un produit**
1. Sélectionnez "Pain" dans la liste
2. Cliquez sur "➕ Ajouter au panier"
3. Vérifiez qu'il apparaît dans le panier

**Test 2 : Vérifier le total**
1. Ajoutez 2 pains
2. Total doit être: 2 × 1.50€ = 3.00€

**Test 3 : Paiement**
1. Sélectionnez "Liquide"
2. Cliquez sur "✅ VALIDER ET PAYER"
3. Message de confirmation doit apparaître

---

## 🚀 ÉTAPE 7 : Déploiement final {#étape-7}

### Objectif
Préparer l'application pour une utilisation en production.

### 7.1 Créer un fichier de lancement

**Créez le fichier :** `run_automaticcheck.bat`

```batch
@echo off
echo ====================================
echo    AutomaticCheck Startup Script
echo ====================================

REM Se positionner dans le bon dossier
cd /d "%~dp0"

REM Activer l'environnement virtuel
call venv\Scripts\activate.bat

REM Lancer le backend dans une nouvelle fenêtre
start "AutomaticCheck Backend" python backend.py

REM Attendre que le serveur démarre
timeout /t 3 /nobreak

REM Lancer le frontend
python frontend.py

REM Garder la fenêtre ouverte
pause
```

**Comment utiliser :**
- Double-cliquez sur `run_automaticcheck.bat`
- L'application démarre automatiquement

### 7.2 Créer un fichier README

**Créez le fichier :** `README.md`

```markdown
# AutomaticCheck - Borne de Caisse Intelligente

## Installation

1. Clonez le projet
2. `python -m venv venv`
3. `.\venv\Scripts\Activate.ps1`
4. `pip install -r requirements.txt`

## Lancement

```powershell
.\venv\Scripts\Activate.ps1
python backend.py
```

Dans une autre fenêtre :
```powershell
.\venv\Scripts\Activate.ps1
python frontend.py
```

## Structure du projet

```
AutomaticCheck_Dev/
├── database.py           # Configuration BD
├── backend.py            # Serveur FastAPI
├── frontend.py           # Interface PyQt6
├── rfid_simulator.py     # Simulateur RFID
├── requirements.txt      # Dépendances
└── automaticcheck.db     # Base de données
```
```

### 7.3 Créer requirements.txt

**Créez le fichier :** `requirements.txt`

```
fastapi==0.104.1
uvicorn==0.24.0
PyQt6==6.6.1
sqlalchemy==2.0.23
python-dateutil==2.8.2
requests==2.31.0
```

**Pour générer automatiquement :**
```powershell
pip freeze > requirements.txt
```

---

## 📚 Commandes utiles

### Démarrer le projet

```powershell
# Terminal 1: Backend
cd "C:\Users\SARA\Desktop\Panier intelligent\AutomaticCheck_Dev"
.\venv\Scripts\Activate.ps1
python backend.py

# Terminal 2: Frontend
cd "C:\Users\SARA\Desktop\Panier intelligent\AutomaticCheck_Dev"
.\venv\Scripts\Activate.ps1
python frontend.py
```

### Réinitialiser la base de données

```powershell
# Supprimer la BD
Remove-Item automaticcheck.db

# Recréer
python database.py
```

### Vérifier l'API

```
http://localhost:8000/docs
```

---

## 🐛 Dépannage

### "Module not found"
```powershell
pip install <nom_du_module>
```

### "ConnectionError"
- Vérifiez que le backend est lancé
- Vérifiez que l'URL est correcte: `http://localhost:8000`

### Base de données vide
```powershell
python database.py
```

---

## 🎓 Concepts clés expliqués

### RFID
**C'est quoi ?** Radio Frequency Identification
**En pratique:** Code unique pour chaque produit (exemple: RFID001)

### FastAPI
**C'est quoi ?** Un serveur web pour votre application
**En pratique:** Reçoit les requêtes du frontend et retourne les données

### PyQt6
**C'est quoi ?** Librairie pour créer des interfaces graphiques
**En pratique:** Ce que vous voyez à l'écran (boutons, texte, etc.)

### SQLite
**C'est quoi ?** Une base de données légère
**En pratique:** Stocke les produits, factures et paiements

---

## 📋 Progression

- [ ] Étape 1 : Environnement ✅
- [ ] Étape 2 : Base de données ✅
- [ ] Étape 3 : Backend ✅
- [ ] Étape 4 : Frontend ✅
- [ ] Étape 5 : RFID ✅
- [ ] Étape 6 : Tests ✅
- [ ] Étape 7 : Déploiement ✅

---

## 💡 Prochaines améliorations possibles

1. **Intégration d'un vrai lecteur RFID USB**
   - Installer `pyserial`
   - Lire depuis le port COM

2. **Interface de gestion des produits**
   - Ajouter/modifier/supprimer des produits
   - Ajuster les prix et stocks

3. **Rapports et statistiques**
   - Ventes par jour
   - Produits les plus vendus
   - Graphiques

4. **Multi-utilisateurs**
   - Comptes de caisse
   - Permissions

5. **Paiement réel**
   - Intégration avec un API de paiement
   - Reçus imprimables

---

**Créé pour : AutomaticCheck Project**  
**Date : 2026**  
**Version : 1.0**
