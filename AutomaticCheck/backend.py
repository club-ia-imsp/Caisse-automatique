import os
import re
from pathlib import Path
import sqlite3
import threading
import time
import serial
from serial.tools import list_ports
from flask import Flask, jsonify, request, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "produits.db"
STATIC_DIR = BASE_DIR / "frontend"
PORT = os.environ.get("RFID_PORT", "COM4")
BAUDRATE = int(os.environ.get("RFID_BAUD", "115200"))
serial_status = "OK"

app = Flask(__name__, static_folder=str(STATIC_DIR), static_url_path="")

cart_items = []
cart_total = 0
cart_lock = threading.Lock()

# Dernière lecture (réussie ou non) afin que l'interface puisse toujours
# afficher un retour visuel quand une carte/étiquette est passée devant le lecteur.
last_scan = {
    "uid": None,
    "found": None,
    "nom": None,
    "prix": None,
    "action": None,
    "source": None,
    "timestamp": None,
}

# L'Arduino renvoie le même UID en boucle (toutes les ~1s) tant que la carte
# reste devant le lecteur. Pour éviter d'ajouter/retirer l'article en boucle,
# on ignore les lectures répétées du même UID pendant ce délai (en secondes).
SCAN_COOLDOWN = 2.0
dernier_scan_par_uid = {}


def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def list_serial_ports():
    return [port.device for port in list_ports.comports()]


def normaliser_uid(uid):
    """Nettoie un UID brut venant du lecteur (espaces, ':', '-', minuscules...)
    pour le ramener au même format que celui stocké en base (ex: '338FE7F7')."""
    return re.sub(r"[^0-9A-Fa-f]", "", uid or "").upper()


def ajouter_uid(uid, source="rfid"):
    global cart_total, last_scan

    uid_normalise = normaliser_uid(uid)
    maintenant = time.time()

    with cart_lock:
        dernier = dernier_scan_par_uid.get(uid_normalise)
        if dernier is not None and (maintenant - dernier) < SCAN_COOLDOWN:
            # Carte encore devant le lecteur : on ignore cette relecture.
            return False, None
        dernier_scan_par_uid[uid_normalise] = maintenant

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT uid, nom, prix, categorie FROM produits WHERE UPPER(uid) = ?", (uid_normalise,))
    produit = cursor.fetchone()
    conn.close()

    if produit is None:
        if source == "rfid":
            print(f"Produit non trouvé pour UID : {uid_normalise or uid}")
        with cart_lock:
            last_scan = {
                "uid": uid_normalise or uid,
                "found": False,
                "nom": None,
                "prix": None,
                "action": None,
                "source": source,
                "timestamp": maintenant,
            }
        return False, None

    item = {
        "uid": produit["uid"],
        "nom": produit["nom"],
        "prix": produit["prix"],
        "categorie": produit["categorie"],
    }

    with cart_lock:
        # Bascule : si l'article est déjà dans le panier, ce passage le retire
        # (décrémente) ; sinon il l'ajoute (incrémente). Cela permet de scanner
        # une fois pour déposer l'article dans le panier et une seconde fois
        # pour le retirer, sans dépendre d'un capteur de sens supplémentaire.
        index_existant = next((i for i, art in enumerate(cart_items) if art["uid"] == item["uid"]), None)
        if index_existant is not None:
            cart_items.pop(index_existant)
            cart_total -= item["prix"]
            action = "retire"
        else:
            cart_items.append(item)
            cart_total += item["prix"]
            action = "ajoute"

        last_scan = {
            "uid": item["uid"],
            "found": True,
            "nom": item["nom"],
            "prix": item["prix"],
            "action": action,
            "source": source,
            "timestamp": maintenant,
        }

    return True, item


@app.route("/")
def index():
    return send_from_directory(STATIC_DIR, "index.html")


@app.route("/api/cart")
def api_cart():
    with cart_lock:
        return jsonify({
            "items": list(cart_items),
            "total": cart_total,
            "serial_status": serial_status,
            "last_scan": dict(last_scan),
        })


@app.route("/api/status")
def api_status():
    return jsonify({
        "serial_status": serial_status,
        "port": PORT,
        "baudrate": BAUDRATE,
        "ports_disponibles": list_serial_ports(),
    })


@app.route("/api/add_uid", methods=["POST"])
def api_add_uid():
    data = request.get_json(silent=True) or {}
    uid = (data.get("uid") or request.form.get("uid") or "").strip()
    if not uid:
        return jsonify({"error": "UID manquant"}), 400

    success, item = ajouter_uid(uid, source="manuel")
    if not success:
        return jsonify({"error": "Aucun produit trouvé pour cet UID"}), 404

    return jsonify(item)


@app.route("/api/simulate_scan", methods=["POST"])
def api_simulate_scan():
    """Simule le passage d'une carte/étiquette devant le lecteur RFID.
    Utile pour tester l'affichage du panier sans avoir le matériel branché."""
    data = request.get_json(silent=True) or {}
    uid = (data.get("uid") or "").strip()

    if not uid:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT uid FROM produits ORDER BY RANDOM() LIMIT 1")
        row = cursor.fetchone()
        conn.close()
        if row is None:
            return jsonify({"error": "Aucun produit en base pour simuler un scan"}), 404
        uid = row["uid"]

    success, item = ajouter_uid(uid, source="simulation")
    if not success:
        return jsonify({"error": "Aucun produit trouvé pour cet UID", "uid": normaliser_uid(uid)}), 404

    return jsonify(item)


@app.route("/api/clear", methods=["POST"])
def api_clear():
    global cart_total
    with cart_lock:
        cart_items.clear()
        cart_total = 0
    return jsonify({"message": "Panier réinitialisé"})


@app.route("/api/pay", methods=["POST"])
def api_pay():
    global cart_total
    with cart_lock:
        if cart_total == 0:
            return jsonify({"error": "Aucun article dans le panier"}), 400
        montant = cart_total
        cart_items.clear()
        cart_total = 0

    return jsonify({"message": "Paiement effectué", "total": montant})


@app.route("/api/products")
def api_products():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT uid, nom, prix, categorie FROM produits ORDER BY nom")
    produits = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return jsonify(produits)


def lecture_rfid():
    """Écoute le port RFID configuré (PORT). On ne tente volontairement PAS
    d'ouvrir d'autres ports série disponibles : le faire bloquerait le thread
    sur un port qui n'est pas le lecteur (ex: un port virtuel/Bluetooth) et
    empêcherait de détecter le vrai lecteur RFID quand il est branché."""
    global serial_status
    while True:
        ports = list_serial_ports()
        if PORT not in ports:
            serial_status = (
                f"En attente du lecteur sur {PORT}"
                f" (ports détectés : {', '.join(ports) if ports else 'aucun'})"
            )
            print(serial_status)
            time.sleep(2)
            continue

        try:
            with serial.Serial(PORT, BAUDRATE, timeout=1) as ser:
                # Sur les cartes ESP32 (reconnaissables ici aux broches GPIO
                # SS_PIN/RST_PIN du sketch), pyserial active DTR/RTS à
                # l'ouverture du port, ce qui maintient la carte en reset et
                # empêche le sketch RFID de s'exécuter (le moniteur série de
                # l'IDE Arduino gère ces lignes différemment, d'où le fait que
                # la lecture y fonctionne mais pas ici). On les relâche pour
                # laisser la carte démarrer normalement.
                try:
                    ser.setDTR(False)
                    ser.setRTS(False)
                except Exception:
                    pass
                time.sleep(1.5)
                ser.reset_input_buffer()

                serial_status = f"OK (port {PORT})"
                print(f"Lecture RFID sur {PORT} à {BAUDRATE} bauds")
                while True:
                    uid = ser.readline().decode(errors="ignore").strip()
                    if uid:
                        print(f"UID scanné : {uid}")
                        ajouter_uid(uid)
        except serial.SerialException as err:
            serial_status = f"Erreur série sur {PORT} : {err}"
            print(serial_status)
            time.sleep(2)
        except Exception as err:
            serial_status = f"Erreur RFID inattendue : {err}"
            print(serial_status)
            time.sleep(2)


def start_rfid_thread():
    thread = threading.Thread(target=lecture_rfid, daemon=True)
    thread.start()


if __name__ == "__main__":
    start_rfid_thread()
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
