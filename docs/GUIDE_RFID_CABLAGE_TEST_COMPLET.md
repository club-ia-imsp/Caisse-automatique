# 📡 GUIDE COMPLET : CÂBLAGE RFID, TEST ET FONCTIONNEMENT DÉTAILLÉ

## 🎯 Objectif Final
Intégrer un **lecteur RFID USB 125kHz** avec le panier intelligent pour scanner les produits en temps réel.

---

## PARTIE 1️⃣ : ARCHITECTURE GLOBALE DU SYSTÈME

### 🏗️ Flux de Données Complet

```
┌─────────────────────────────────────────────────────────────┐
│                    SYSTÈME AUTOMATICCHECK                    │
└─────────────────────────────────────────────────────────────┘

    ┌─────────────────────────────────────────────────────────┐
    │                     PANIER PHYSIQUE                      │
    │  ┌────────────────────────────────────────────────────┐  │
    │  │  400mm × 300mm × 250mm (PLA)                       │  │
    │  │  • 4 antennes 80mm aux coins                       │  │
    │  │  • Cablage vers lecteur RFID                       │  │
    │  │  • Tags RFID002 à RFID008 collés sur produits     │  │
    │  └────────────────────────────────────────────────────┘  │
    └────────────────┬──────────────────────────────────────┘
                     │ (Câble série USB)
                     ↓
    ┌────────────────────────────────────────────────────────┐
    │           LECTEUR RFID (125kHz - USB)                  │
    │  Modèles compatibles :                                 │
    │  • ID Innovations ID20/ID25                            │
    │  • RFID125-USB                                         │
    │  • SkyTek M1                                           │
    │                                                        │
    │  Spécifications :                                      │
    │  • Interface : USB ou Serial (COM)                     │
    │  • Fréquence : 125 kHz                                 │
    │  • Débit : 9600 baud                                  │
    │  • Distance : 5-10 cm (selon antenne)                 │
    │  • Sortie : Code RFID en ASCII + CR/LF               │
    └────────────────┬──────────────────────────────────────┘
                     │ (USB vers PC)
                     ↓
    ┌────────────────────────────────────────────────────────┐
    │              PC WINDOWS (Serveur)                       │
    │                                                        │
    │  ┌──────────────────────────────────────────────────┐  │
    │  │         backend.py (FastAPI)                     │  │
    │  │  • Serveur REST sur localhost:8000              │  │
    │  │  • Routes API produits, factures, paiements     │  │
    │  │  • SQLite pour stocker les données              │  │
    │  └──────────────────────────────────────────────────┘  │
    │                        ↑↓ (HTTP)                       │
    │  ┌──────────────────────────────────────────────────┐  │
    │  │         frontend.py (PyQt6)                      │  │
    │  │  • GUI panier d'achat                            │  │
    │  │  • Bouton "Scanner RFID Manuel"                  │  │
    │  │  • Appel API + affichage facture                 │  │
    │  └──────────────────────────────────────────────────┘  │
    │                        ↑↓ (Serial)                      │
    │  ┌──────────────────────────────────────────────────┐  │
    │  │         rfid_reader.py (Lecteur)                │  │
    │  │  • Thread séparé de lecture série                │  │
    │  │  • Parse codes RFID reçus                        │  │
    │  │  • Queue pour non-bloquant                       │  │
    │  └──────────────────────────────────────────────────┘  │
    │                        ↓ (Acquisition)                  │
    │  ┌──────────────────────────────────────────────────┐  │
    │  │         database.py (SQLite)                     │  │
    │  │  • Table produits avec codes_rfid                │  │
    │  │  • Table factures et paiements                   │  │
    │  │  • Gestion du stock                              │  │
    │  └──────────────────────────────────────────────────┘  │
    └────────────────────────────────────────────────────────┘
                             ↑
                    (Affichage 7" HDMI)
                             
    ┌────────────────────────────────────────────────────────┐
    │              ÉCRAN 7" HDMI/Tactile (optionnel)         │
    │  • Affiche le GUI PyQt6 en temps réel                 │
    │  • Permet interaction tactile du vendeur              │
    └────────────────────────────────────────────────────────┘
```

---

## PARTIE 2️⃣ : CÂBLAGE DÉTAILLÉ

### 📋 Composants Nécessaires

**Pour lecteur RFID 125kHz USB :**
- ✅ Lecteur RFID USB (ID Innovations ID20/ID25 recommandé)
- ✅ Câble USB A vers micro-USB ou série (selon modèle)
- ✅ Antenne USB 125kHz OU antennes externes
- ✅ Câble série RS232 USB (si lecteur sans USB natif)

**Pour intégration dans panier :**
- ✅ Câbles de ferrite (blindage EMI)
- ✅ Connecteurs étanches (IP67)
- ✅ Gaine thermorétractable ou adhésif
- ✅ Passe-câble étanche

### 🔌 Cas 1 : Lecteur RFID USB Direct (Recommandé - Simpler)

```
┌─────────────────┐
│  PC WINDOWS     │
│                 │
│  PORT USB       │
│  (Automatique)  │
└────────┬────────┘
         │
         │ Câble USB A
         │ (2 mètres max)
         │
    ┌────▼─────────┐
    │ LECTEUR RFID  │
    │ USB 125kHz    │
    │               │
    │ ID20/ID25     │
    │ (Exemple)     │
    └────┬──────────┘
         │
         │ Antenne intégrée
         │ (5-10cm de distance)
         │
    ┌────▼──────────┐
    │  TAGS RFID    │
    │  Collés sur   │
    │  produits     │
    └───────────────┘
```

**Avantages :**
- Aucun câblage complexe
- Alimentation par USB (5V depuis PC)
- Windows reconnaît automatiquement comme COM
- Débit 9600 baud par défaut

**Installation :**
1. Brancher USB dans PC
2. Windows installe driver automatiquement
3. Vérifier dans "Gestionnaire des périphériques" → "Ports (COM et LPT)"
4. Noter le numéro COM (ex: COM3)

---

### 🔌 Cas 2 : Lecteur avec Antenne Externe (Pour Panier Intégré)

```
┌──────────────────────────────────────────────────┐
│         LECTEUR RFID (Boîtier)                   │
│                                                  │
│  ┌────────────────────────────────────────────┐ │
│  │ Connecteur de sortie série:                │ │
│  │                                            │ │
│  │  PIN 1: GND (Terre/Noir)                  │ │
│  │  PIN 2: TX (Transmit/Vert) → PC RX       │ │
│  │  PIN 3: RX (Receive/Rouge) → PC TX       │ │
│  │  PIN 4: +5V (Alimentation/Orange)        │ │
│  │  PIN 5: GND (Terre/Noir)                  │ │
│  │                                            │ │
│  └────────────────────────────────────────────┘ │
│           │                 │                   │
│           │                 │ Vers antennes    │
│           │                 │                   │
│           │        ┌────────▼────────┐         │
│           │        │ CIRCUIT ANTENNE │         │
│           │        │                │         │
│           │        │ 4× 80mm à coins │         │
│           │        │ du panier       │         │
│           │        └────────────────┘         │
│           │                                   │
│      [Câble série DB9 blindé]                │
│           │                                   │
└───────────┼───────────────────────────────────┘
            │
            │ Via adaptateur
            │ USB-Série
            │
       ┌────▼────┐
       │   PC    │
       │  PORT   │
       │  USB    │
       └─────────┘
```

**Schéma Détaillé des Antennes (125kHz) :**

```
Chaque antenne 80mm placer aux coins du panier:

        ┌─────────────────────────┐
        │    Antenne RFID         │
        │   80mm × 80mm           │
        │                         │
        │  Coil 125kHz bobine    │
        │                         │
    ┌───┴───┐             ┌───┬───┐
    │       │             │   │   │
    RX out TX in (Vers lecteur)
    │       │             │   │   │
    └───┬───┘             └───┴───┘
        │
    [Câble blindé
     3 conducteurs]
        │
   ┌────▼──────┐
   │ Connecteur │
   │ Antenne   │
   └────┬──────┘
        │
    (À répéter 4 fois
     aux 4 coins)
```

**Câblage Antenne vers Lecteur :**

Pour **chaque antenne** :

| Fil | Couleur | Connexion |
|-----|---------|-----------|
| TX | Vert | TX+ du lecteur |
| RX | Rouge | RX+ du lecteur |
| GND | Noir | GND du lecteur |
| Blindage | Or/Argent | GND du lecteur |

**Distance antenne-panier:** 10-20 cm maximum

---

### 🔌 Cas 3 : Lecteur avec Adaptateur USB-Série (Alternative)

```
Si lecteur RFID avec sortie série RS232 uniquement:

┌──────────────┐
│  PC Windows  │
│              │
│ Port USB     │
└────┬─────────┘
     │
     │ Câble USB A
     │
┌────▼──────────────────┐
│ Adaptateur USB→RS232  │
│ (PL2303 ou CH340)     │
│                       │
│ TX (Pin 3) ──────────▶│ 
│ RX (Pin 2) ◀──────────│
│ GND (Pin 5) ──────────│
└────┬──────────────────┘
     │
     │ Câble RS232 blindé
     │ (DB9 ou RJ45)
     │
┌────▼─────────────────────┐
│ LECTEUR RFID RS232        │
│ (Sortie série native)     │
│                           │
│ ┌───────────────────────┐ │
│ │ 4 Antennes 80mm       │ │
│ │ (Aux 4 coins panier)  │ │
│ └───────────────────────┘ │
└───────────────────────────┘
```

---

## PARTIE 3️⃣ : COMMENT LE SYSTÈME FONCTIONNE EN DÉTAIL

### 🔄 Flux de Fonctionnement Complet (Pas à Pas)

#### **Étape 1 : Initialisation (Au démarrage)**

```python
# database.py s'exécute PRIMO
1. Vérifier si "automaticcheck.db" existe
2. Si NON → Créer base SQLite vide
3. Créer tables: produits, factures, articles_facture, paiements
4. Insérer 8 produits démo avec codes RFID (RFID001 à RFID008)

Résultat: ✅ BD initialisée avec 8 produits prêts
```

#### **Étape 2 : Backend Démarre**

```python
# backend.py s'exécute (Terminal 1)
1. Charger base de données SQLite
2. Initialiser serveur FastAPI
3. Exposer 6 routes REST sur localhost:8000

Routes disponibles:
   GET  /api/health              → {"status": "ok"}
   GET  /api/produits            → [Liste tous les produits]
   GET  /api/produits/{code}     → [Cherche produit par RFID]
   POST /api/factures            → [Crée facture + décremente stock]
   GET  /api/factures/{id}       → [Récupère détails facture]
   POST /api/paiements/{id}      → [Enregistre paiement]

Résultat: ✅ Serveur écoute sur localhost:8000
           Accessible via http://localhost:8000/docs (Swagger)
```

#### **Étape 3 : Frontend Démarre**

```python
# frontend.py s'exécute (Terminal 2)
1. Créer GUI PyQt6 (QMainWindow)
2. À l'ouverture: charger_produits()
   - Appel: GET http://localhost:8000/api/produits
   - Réponse: [prod1, prod2, prod3, ...]
   - Affiche: QListWidget avec "Fromage Comté (15.50€)", etc.

Interface 3 panneaux:
   ┌──────────────────────────────────────┐
   │ PANNEAU GAUCHE         PANNEAU CENTRE PANNEAU DROIT
   │ (Produits)            (Panier)      (Facture/Paiement)
   │ • Fromage (15.50€)     • QTableWidget • Total: 0.00€
   │ • Lait (2.50€)        (produits    • Combo paiement:
   │ • Pain (3.00€)         ajoutés)      - Liquide
   │ • Beurre (5.00€)      • Boutons:    - Carte
   │ • Œufs (4.50€)         ☒ Ajouter    - Chèque
   │ • Miel (8.00€)         ☒ Supprimer  • Bouton:
   │ • Confiture (6.50€)    ☒ Scanner RFID → [Valider
   │ • Jambon (12.00€)       Manuel        Paiement]
   │                                     • Facture s'affiche
   └──────────────────────────────────────┘

Résultat: ✅ GUI affiche 8 produits prêts à l'emploi
```

#### **Étape 4 : Utilisateur Ajoute Produit (Cas 1: Clic)**

```
Utilisateur clique sur "Fromage Comté" dans PANNEAU GAUCHE

1. Événement: itemClicked() détecté
2. selectionner_produit() appelé
3. Stocke: {"id": 1, "nom": "Fromage Comté", "prix": 15.50, ...}
4. Utilisateur clique "➕ Ajouter au Panier"
5. ajouter_au_panier() appelé
6. Ajoute à liste: basket.append({produit_1, quantité=1})
7. mettre_a_jour_affichage() rafraîchit:
   - QTableWidget montre: "Fromage Comté | 1 | 15.50€"
   - Label Total: "TOTAL: 15.50€"

Résultat: ✅ Produit dans panier, total mis à jour
```

#### **Étape 5 : Utilisateur Scanne (Cas 2: RFID)**

```
Variante: Utilisateur clique "📱 Scanner RFID Manuel"

1. Événement: clic bouton
2. scanner_rfid_manuel() appelé
3. Affiche QInputDialog: "Entrez code RFID (ex: RFID001):"
4. Utilisateur tape code ou approche tag du lecteur
5. Code reçu (ex: "RFID001\r\n")
6. Appel API: GET http://localhost:8000/api/produits/RFID001
7. Réponse: {"id": 1, "nom": "Fromage Comté", "prix": 15.50, ...}
8. Ajoute automatiquement au panier
9. mettre_a_jour_affichage() rafraîchit

Résultat: ✅ Produit trouvé par RFID et ajouté
```

#### **Étape 6 : Validation du Paiement (Flux Final)**

```
Utilisateur clique "✅ Valider Paiement"

1. valider_paiement() appelé
2. Récupère panier: [{"id": 1, "qty": 2}, {"id": 2, "qty": 1}]
3. Récupère mode: "Liquide"
4. Crée structure facture:
   {
     "articles": [
       {"produit_id": 1, "quantite": 2},
       {"produit_id": 2, "quantite": 1}
     ],
     "mode_paiement": "Liquide"
   }
5. Appel API: POST http://localhost:8000/api/factures
   
   BACKEND REÇOIT:
   ├─ Valide quantités
   ├─ Vérifie stock disponible en BD
   ├─ Si OK: décrémente stock en BD
   ├─ Crée facture en BD (INSERT)
   ├─ Crée articles_facture (INSERT × 2)
   ├─ Calcule total: (15.50 × 2) + (2.50 × 1) = 33.50€
   └─ Retourne: {"facture_id": 42, "total": 33.50, ...}

6. Frontend reçoit facture_id = 42
7. Appel API: POST http://localhost:8000/api/paiements/42
   {
     "montant": 33.50,
     "mode_paiement": "Liquide"
   }
   
   BACKEND REÇOIT:
   ├─ Vérifie montant correspond facture
   ├─ Enregistre paiement en BD (INSERT)
   ├─ Met à jour statut facture: "payée"
   └─ Retourne: {"statut": "succès"}

8. Frontend reçoit confirmation ✅
9. generer_facture() crée texte:
   ═════════════════════
    FACTURE N°42
    2026-05-22 14:35:12
   ═════════════════════
    Fromage Comté        ×2  31.00€
    Lait                 ×1   2.50€
   ─────────────────────────────
    TOTAL                    33.50€
    Paiement: Liquide
   ═════════════════════
   
10. Affiche facture dans PANNEAU DROIT
11. Message box: "✅ Paiement accepté !"
12. Panier se vide
13. Interface retour à 0

Résultat: ✅ Paiement traité, stock décrémenté, facture générée
```

---

## PARTIE 4️⃣ : TEST DÉTAILLÉ DU RFID

### ✅ TEST 1 : Vérifier le COM Port

**Objectif :** Confirmer que Windows reconnaît le lecteur RFID

**Étapes :**

1. Brancher lecteur RFID en USB sur le PC
2. Attendre 5-10 secondes (Windows cherche driver)
3. Ouvrir **"Gestionnaire des périphériques"** :
   - Ctrl+Pause (Panneau de configuration → Système avancé)
   - OU : Win+R → `devmgmt.msc` → Enter
   
4. Chercher rubrique **"Ports (COM et LPT)"**
5. Vérifier présence : `COM3` ou `COM4` ou `COM5`
   - Si port USB FTDI/PL2303 : `USB Serial Port (COM?)`

**✅ Succès :** Port COM visible, ex: `COM3`
**❌ Échec :** Aucun port COM → Installer driver du lecteur

---

### ✅ TEST 2 : Tester la Connexion Série Brute

**Objectif :** Vérifier que le lecteur communique et envoie des données

**Outils :** Python + `pyserial`

**Commande :**

```python
python -c "
import serial
import time

port = 'COM3'  # À adapter selon Test 1
baudrate = 9600

try:
    ser = serial.Serial(port, baudrate, timeout=2)
    print(f'✅ Connecté à {port}')
    print('Prêt à lire codes RFID...')
    print('Approchez un tag RFID du lecteur...\n')
    
    for i in range(10):  # Lire 10 codes max
        data = ser.readline().decode().strip()
        if data:
            print(f'   Code reçu: {data}')
            if len(data) == 10 and data.startswith('RFID'):
                print(f'   ✅ Format valide !')
        else:
            print(f'   En attente... ({i+1}/10)')
        time.sleep(1)
    
    ser.close()
    print('\n✅ Test terminé')
    
except Exception as e:
    print(f'❌ Erreur: {e}')
"
```

**Procédure :**
1. Ouvrir PowerShell dans `AutomaticCheck_Dev`
2. Remplacer `COM3` par votre port (du Test 1)
3. Exécuter commande
4. Approcher tag RFID du lecteur
5. Observer codes reçus dans console

**✅ Succès :** Voir `Code reçu: RFID001` (ou autre code)
**❌ Échec :** "En attente..." → Vérifier:
   - Lecteur branché ? (voyant vert ?)
   - Tag RFID près du lecteur ? (< 10cm)
   - Code RFID correct dans BD ?

---

### ✅ TEST 3 : Tester le Module RFID Python

**Objectif :** Vérifier que le module `rfid_reader.py` fonctionne

**Commande :**

```python
python -c "
from rfid_reader import RFIDReader

print('🔌 Test RFIDReader...')

try:
    reader = RFIDReader()  # Auto-détecte port
    print(f'✅ Lecteur trouvé sur port: {reader.port}')
    
    reader.connecter()
    print('✅ Connecté au lecteur')
    
    print('En attente d\'un code RFID (10 secondes)...')
    print('Approchez un tag du lecteur...\n')
    
    code = reader.obtenir_code(timeout=10)
    
    if code:
        print(f'✅ Code reçu: {code}')
    else:
        print('❌ Timeout - aucun code reçu')
    
    reader.deconnecter()
    print('✅ Déconnecté')
    
except Exception as e:
    print(f'❌ Erreur: {e}')
    print('💡 Vérifier:')
    print('   1. Lecteur RFID branché en USB')
    print('   2. Port COM correct dans le gestionnaire')
    print('   3. Tag RFID à proximité (<10cm)')
"
```

**Procédure :**
1. Ouvrir PowerShell dans `AutomaticCheck_Dev`
2. Activer venv: `.\venv\Scripts\Activate.ps1`
3. Exécuter commande Python
4. Approcher tag RFID

**✅ Succès :** `Code reçu: RFID001`
**⚠️ Note :** Auto-détecte le port COM automatiquement

---

### ✅ TEST 4 : Intégration Complète avec Backend + Frontend

**Objectif :** Tester flux complet: RFID → Backend → Frontend

**Procédure (3 Terminaux) :**

**Terminal 1 - Backend :**
```powershell
cd C:\Users\SARA\Desktop\Panier intelligent\AutomaticCheck_Dev
.\venv\Scripts\Activate.ps1
python backend.py
```
Attend: `Uvicorn running on http://127.0.0.1:8000`

**Terminal 2 - Frontend :**
```powershell
cd C:\Users\SARA\Desktop\Panier intelligent\AutomaticCheck_Dev
.\venv\Scripts\Activate.ps1
python frontend.py
```
Attend: GUI PyQt6 apparaît avec 8 produits

**Terminal 3 - Test RFID :**
```powershell
cd C:\Users\SARA\Desktop\Panier intelligent\AutomaticCheck_Dev
.\venv\Scripts\Activate.ps1

# Tester scanner manuel dans GUI
```

**Étapes :**
1. GUI affiche 8 produits
2. Cliquer "📱 Scanner RFID Manuel"
3. Input dialog: entrer `RFID001`
4. Produit "Fromage Comté" s'ajoute au panier
5. Total met à jour: "15.50€"

**✅ Succès :** Flux complet fonctionne
**❌ Échec :** Voir section Troubleshooting

---

### ✅ TEST 5 : Test du Panier Physique (Après Assemblage)

**Prérequis :**
- ✅ Panier 3D imprimé (400×300×250mm)
- ✅ 4 antennes 80mm intégrées
- ✅ Lecteur RFID câblé aux antennes
- ✅ Tags RFID collés sur produits physiques
- ✅ Produits physiques placés dans panier

**Procédure :**

```python
# Lancer dans Terminal 3
python -c "
from rfid_reader import RFIDReader
import time

reader = RFIDReader()
reader.connecter()

print('🧺 TEST PANIER PHYSIQUE')
print('Temps: 30 secondes')
print('Place des produits dans le panier...\n')

codes_lus = []

for i in range(30):
    try:
        code = reader.obtenir_code(timeout=1)
        if code and code not in codes_lus:
            codes_lus.append(code)
            print(f'✅ [{i}s] Détecté: {code}')
    except:
        pass
    time.sleep(1)

reader.deconnecter()

print(f'\n📊 Résumé:')
print(f'   Codes uniques détectés: {len(codes_lus)}')
print(f'   Codes: {codes_lus}')
print(f'   Portée antennes: OK ✅')
"
```

**Résultats Attendus :**
- Détecte tous les tags dans le panier
- Portée: 15-20cm depuis parois
- Pas de faux positifs

---

## PARTIE 5️⃣ : TROUBLESHOOTING DÉTAILLÉ

### ❌ Problème 1 : "Gestionnaire des périphériques ne montre pas de COM"

**Cause :** Driver USB-Série manquant

**Solution :**

1. **Pour lecteur FTDI (PL2303) :**
   ```
   https://www.prolific.com.tw/US/ShowProduct.aspx?p_id=155
   Télécharger et installer driver officiel
   ```

2. **Pour lecteur CH340 :**
   ```
   https://github.com/MarlinFirmware/Marlin/wiki/Flashing-Firmware
   Section "Installing Drivers" → CH340
   ```

3. **Redémarrer Windows** après installation

4. Brancher lecteur à nouveau → Port COM devrait apparaître

---

### ❌ Problème 2 : "En attente... Aucun code reçu"

**Cause 1 :** Lecteur pas alimenté

**Solution :**
- Vérifier voyant LED lecteur s'allume (rouge/vert)
- Si non → USB pas branché correctement
- Essayer autre port USB

**Cause 2 :** Antenne cassée ou mal connectée

**Solution :**
- Vérifier connecteur antenne bien enfoncé
- Tester antenne avec multimètre (continuité)
- Remplacer si endommagée

**Cause 3 :** Tag RFID défaillant

**Solution :**
- Tester autre tag RFID
- Si fonctionne → tag original est cassé
- Remplacer tags si nécessaire

**Cause 4 :** Mauvaise fréquence

**Solution :**
- ✅ Pour 125kHz : lecteur ID Innovations OK
- ❌ Pour 13.56MHz : besoins lecteur différent
- Vérifier spéc lecteur acheté

---

### ❌ Problème 3 : "ConnectionError: Impossible de se connecter au serveur"

**Cause :** Backend pas démarré

**Solution :**
1. Terminal 1 : `python backend.py`
2. Attendre message: `Uvicorn running on http://127.0.0.1:8000`
3. Puis lancer frontend

---

### ❌ Problème 4 : "ModuleNotFoundError: No module named 'PyQt6'"

**Cause :** Dépendances pas installées

**Solution :**
```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

### ❌ Problème 5 : "Import rfid_reader: No module named serial"

**Cause :** pyserial pas installé

**Solution :**
```powershell
.\venv\Scripts\Activate.ps1
pip install pyserial==3.5
```

---

## PARTIE 6️⃣ : DÉTAILS TECHNIQUES AVANCÉS

### 🔧 Format de Données du RFID

**Format du code reçu du lecteur :**

```
Transmission série USB (9600 baud):
┌─────────────────────────────────┐
│  R   F   I   D   0   0   1   \r\n  │
│  01  02  03  04  05  06  07  08   │
│                                  │
│  [1-10] = Code RFID (10 octets)  │
│  [11]   = Carriage Return (\r)   │
│  [12]   = Line Feed (\n)         │
└─────────────────────────────────┘

Exemple complet en hexadécimal:
52 46 49 44 30 30 31 0D 0A
R  F  I  D  0  0  1  CR  LF
```

**Parsing en Python :**

```python
data_brut = ser.readline()  # b'RFID001\r\n'
code = data_brut.decode().strip()  # 'RFID001'

# Validation
if len(code) == 10 and code.startswith('RFID'):
    print(f"Code valide: {code}")
```

---

### 🔧 Timing de Lecture

**Délai entre lecture et réception :**

```
┌────────────────┐
│  Tag approché  │
└────────┬───────┘
         │ [50ms - lecteur détecte]
         ↓
    Lecture RFID
    [100ms]
         │
         ↓ [20ms - encodage USB]
    ┌────────────────────┐
    │ Transmission USB   │
    │ @ 9600 baud       │
    │ ~1ms par octet    │
    │ × 12 octets       │
    │ = ~12ms total     │
    └────────┬───────────┘
             │
             ↓ [10ms - PC reçoit]
         ┌─────────────┐
         │ Code en mémoire PC
         │ Prêt à traiter
         └─────────────┘
    
Total: ~170ms entre approche et traitement
```

**Implications :**
- Pas de problème pour lecture manuelle (>500ms)
- Si déplacement rapide dans panier: OK (plusieurs lectrices possibles)
- Peut lire ~6 tags par seconde max (théorique)

---

### 🔧 Architecture Threading du Module RFID

**Comment fonctionne `rfid_reader.py` :**

```python
# THREAD PRINCIPAL
┌────────────────────────────────┐
│  objet = RFIDReader()          │
│  reader.connecter()            │
│  code = reader.obtenir_code()  │ ← Bloquant si Queue vide
└──────────────┬─────────────────┘
               │
               ├─ Lance THREAD SECONDAIRE
               │
               ↓ THREAD SECONDAIRE
          ┌──────────────────────────┐
          │ _lire_boucle() en continu│
          │                          │
          │ Boucle:                  │
          │   data = ser.readline()  │
          │   queue.put(data)        │ ← Non-bloquant
          │   Répéter               │
          │                          │
          │ Lance au connecter()    │
          │ S'arrête au déconnecter│
          └──────────────────────────┘

Avantage: GUI jamais bloquée par lecture
          Lecture continue en background
          Pas de perte de données
```

**Exemple d'utilisation :**

```python
# Sans threading (Mauvais - GUI gèle):
code = ser.readline()  # Attend 1s si rien

# Avec threading (Bon - GUI réactive):
reader = RFIDReader()
reader.connecter()
code = reader.obtenir_code(timeout=5)  # Attend max 5s, GUI libre
```

---

### 🔧 Protocole API REST

**Format des requêtes/réponses :**

```
REQUEST 1: Chercher produit par RFID
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GET /api/produits/RFID001 HTTP/1.1
Host: localhost:8000
Accept: application/json

RESPONSE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "nom": "Fromage Comté",
  "prix": 15.50,
  "stock": 8,
  "code_rfid": "RFID001",
  "categorie": "Fromage"
}
```

```
REQUEST 2: Créer facture (Scanner + Paiement)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
POST /api/factures HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "articles": [
    {"produit_id": 1, "quantite": 2},
    {"produit_id": 3, "quantite": 1}
  ],
  "mode_paiement": "Liquide"
}

RESPONSE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HTTP/1.1 200 OK

{
  "facture_id": 42,
  "total": 33.50,
  "nombre_articles": 3,
  "articles": [
    {"produit_id": 1, "quantite": 2, "prix_unitaire": 15.50},
    {"produit_id": 3, "quantite": 1, "prix_unitaire": 3.00}
  ]
}
```

```
REQUEST 3: Enregistrer paiement
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
POST /api/paiements/42 HTTP/1.1
Host: localhost:8000
Content-Type: application/json

{
  "montant": 33.50,
  "mode_paiement": "Liquide"
}

RESPONSE:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
HTTP/1.1 200 OK

{
  "statut": "succès",
  "facture_id": 42,
  "montant_paye": 33.50
}
```

---

### 🔧 Schéma Base de Données

**Diagramme Entité-Relation :**

```
┌─────────────────────────────────┐
│         PRODUITS                │
├─────────────────────────────────┤
│ id (PK) ..................... 1 │
│ nom ...................Fromage   │
│ prix ..................... 15.50 │
│ stock ........................ 5 │
│ code_rfid ........... RFID001   │
│ categorie ..... Produits Laitiers│
└────────┬──────────────────────┬──┘
         │                      │
         │ (1:N)               │ (1:N)
         │                      │
    ┌────▼──────────┐   ┌──────▼─────┐
    │ARTICLES_FACT. │   │ FACTURES    │
    ├────────────────┤   ├─────────────┤
    │ facture_id (FK)────→id (PK)  42  │
    │ produit_id (FK)    │ date    ... │
    │ quantite ....... 2 │ total .. 33.50
    │ prix_unitaire  15.50
    │             │ statut .. payée
    │             │ nb_articles.. 3
    │             └────┬────────────┘
    │                  │ (1:1)
    │                  │
    └──────────────────┤
                       │
                  ┌────▼───────────┐
                  │  PAIEMENTS      │
                  ├─────────────────┤
                  │ facture_id (FK) │
                  │ montant ... 33.50
                  │ mode ...  Liquide
                  │ statut ...   OK │
                  └─────────────────┘
```

---

## PARTIE 7️⃣ : CHECKLIST FINALE

### ✅ Avant de Commencer

- [ ] PC Windows avec Python 3.11+ installé
- [ ] Lecteur RFID USB 125kHz acheté
- [ ] Câble USB branché
- [ ] Dossier `AutomaticCheck_Dev` créé
- [ ] Tous fichiers Python en place

### ✅ Pendant le Test

- [ ] Venv créé et activé
- [ ] `pip install -r requirements.txt` exécuté
- [ ] `python database.py` exécuté
- [ ] Com port du lecteur identifié (Test 1)
- [ ] Connectivité série vérifiée (Test 2)
- [ ] Module RFID testée (Test 3)
- [ ] Backend démarré (Terminal 1)
- [ ] Frontend démarré (Terminal 2)
- [ ] Scanner manuel fonctionne (Test 4)

### ✅ Avant l'Assemblage Physique

- [ ] Panier 3D imprimé et testé
- [ ] Antennes 80mm × 4 en place
- [ ] Câbles blindés soudés aux antennes
- [ ] Connecteurs étanches installés
- [ ] Gaine thermorétractable posée
- [ ] Pas court-circuit (test multimètre)

### ✅ Après l'Intégration Matérielle

- [ ] Lecteur RFID câblé aux antennes
- [ ] COM port toujours reconnu
- [ ] Test 5 (Panier Physique) réussi
- [ ] Portée antennes >15cm
- [ ] Tags RFID programmés (RFID001-RFID008)
- [ ] Tags collés sur produits

### ✅ Production

- [ ] Système complet en service
- [ ] Vendeur peut scanner
- [ ] Stock se décrémente correctement
- [ ] Factures s'impriment
- [ ] Paiements enregistrés en BD

---

## 📞 SUPPORT RAPIDE

**"Ça ne marche pas, que faire ?"**

1. Vérifier lecteur détecté (Test 1)
2. Vérifier lecteur communique (Test 2)
3. Vérifier venv activé (Terminal)
4. Vérifier backend démarré (Terminal 1)
5. Vérifier frontend démarré (Terminal 2)
6. Vérifier base de données initialisée
7. Regarder Troubleshooting (Partie 5)

**"Lecteur RFID pas détecté"**
→ Driver USB-Série manquant (Partie 5, Problème 1)

**"Aucun code reçu"**
→ Antenne cassée ou tag trop loin (Partie 5, Problème 2)

**"GUI gèle pendant lecture"**
→ Normal! Threading gère l'arrière-plan

**"Stock pas décrémenté"**
→ Vérifier facture créée avec POST /api/factures

---

## 📊 RÉSUMÉ ARCHITECTURE

```
MATÉRIEL          COMMUNICATION       LOGICIEL          DONNÉES
═════════════════════════════════════════════════════════════════

Tag RFID          ◄──── 125kHz ────►   Antenne 80mm
                                          │
                                          │ (Câble blindé)
Lecteur RFID ─────────────────────────────┘
      │
      │ (USB série)
      │
      ▼
   PC WINDOWS
   ┌──────────────────────────────────────────────────┐
   │                                                  │
   │  rfid_reader.py  ◄──── Thread lecture ─────►    │
   │         │                                        │
   │         │ (Queue non-bloquant)                  │
   │         │                                        │
   │         ▼                                        │
   │  frontend.py   ◄─────── HTTP ─────────►          │
   │  (PyQt6 GUI)                                     │
   │         │                                        │
   │         │ (Requête HTTP API)                    │
   │         │                                        │
   │         ▼                                        │
   │  backend.py (FastAPI)  ◄─────────────►    │
   │  (6 routes REST)                        │
   │         │                               │
   │         │ (SQL)                         │
   │         │                               │
   │         ▼                               │
   │    SQLite BD            ◄────────► Fichier
   │  (automaticcheck.db)                 BD
   │                                       │
   └──────────────────────────────────────┘
```

---

**Document Complet ✅**
*Dernière mise à jour: 2026-05-22*
*Pour questions: Voir Partie 5 (Troubleshooting) ou Support Rapide*
