import serial
import threading
import sqlite3
import tkinter as tk
from pathlib import Path
from tkinter import messagebox

BASE_DIR = Path(__file__).resolve().parent

# ==========================
# CONFIGURATION
# ==========================

PORT = "COM4"
BAUDRATE = 115200

# ==========================
# VARIABLES
# ==========================

panier = []
total = 0

# ==========================
# BASE DE DONNEES
# ==========================

def rechercher_produit(uid):

    conn = sqlite3.connect(BASE_DIR / "produits.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT nom, prix FROM produits WHERE uid=?",
        (uid,)
    )

    produit = cursor.fetchone()

    conn.close()

    return produit

# ==========================
# PANIER
# ==========================

def ajouter_produit(uid):

    global total

    produit = rechercher_produit(uid)

    if produit:

        nom, prix = produit

        panier.append((nom, prix))

        liste.insert(
            tk.END,
            f"{nom} - {prix} FCFA"
        )

        total += prix

        total_label.config(
            text=f"TOTAL : {total} FCFA"
        )

        empty_label.place_forget()

    else:

        messagebox.showwarning(
            "Produit inconnu",
            f"Aucun produit associé à : {uid}"
        )


def vider_panier():

    global total

    panier.clear()

    liste.delete(0, tk.END)

    total = 0

    total_label.config(
        text="TOTAL : 0 FCFA"
    )

    empty_label.place(relx=0.5, rely=0.5, anchor="center")


def payer():

    global total

    if total == 0:

        messagebox.showinfo(
            "Panier vide",
            "Aucun article dans le panier"
        )

        return

    messagebox.showinfo(
        "Paiement",
        f"Paiement effectué\n\nMontant : {total} FCFA"
    )

    vider_panier()

# ==========================
# RFID
# ==========================

def lecture_rfid():

    try:

        ser = serial.Serial(
            PORT,
            BAUDRATE,
            timeout=1
        )

        while True:

            uid = (
                ser.readline()
                .decode(errors="ignore")
                .strip()
            )

            if uid:

                print("Carte détectée :", uid)

                fenetre.after(
                    0,
                    ajouter_produit,
                    uid
                )

    except Exception as e:

        messagebox.showerror(
            "Erreur série",
            str(e)
        )

# ==========================
# INTERFACE
# ==========================

fenetre = tk.Tk()
fenetre.title("AutomaticCheck")
fenetre.geometry("420x760")
fenetre.configure(bg="#E6F4EF")
fenetre.resizable(False, False)

header_frame = tk.Frame(
    fenetre,
    bg="#1E8F5D",
    padx=20,
    pady=20
)
header_frame.pack(fill=tk.X)

titre = tk.Label(
    header_frame,
    text="AutomaticCheck",
    fg="white",
    bg="#1E8F5D",
    font=("Arial", 24, "bold")
)

titre.pack(anchor="w")

subtitle = tk.Label(
    header_frame,
    text="Scanner RFID → facture → paiement",
    fg="#D8F0E4",
    bg="#1E8F5D",
    font=("Arial", 11)
)

subtitle.pack(anchor="w", pady=(5, 0))

scanner_card = tk.Frame(
    fenetre,
    bg="white",
    bd=0,
    highlightbackground="#B5E2CE",
    highlightthickness=1,
    padx=16,
    pady=18
)
scanner_card.pack(fill=tk.X, padx=16, pady=(20, 10))

scanner_title = tk.Label(
    scanner_card,
    text="Passer un tag RFID",
    font=("Arial", 14, "bold"),
    bg="white",
    fg="#1D5E42"
)

scanner_title.pack(anchor="w")

scanner_message = tk.Label(
    scanner_card,
    text="Le lecteur RFID est en écoute automatique.\nScannez une carte ou un tag, l'ajout se fait seul.",
    font=("Arial", 11),
    bg="#F7FBF9",
    fg="#4F6959",
    justify="left",
    wraplength=360,
    padx=12,
    pady=12
)

scanner_message.pack(fill=tk.X, pady=(12, 0))

summary_card = tk.Frame(
    fenetre,
    bg="white",
    bd=0,
    highlightbackground="#B5E2CE",
    highlightthickness=1,
    padx=16,
    pady=18
)
summary_card.pack(fill=tk.BOTH, expand=True, padx=16, pady=(0, 10))

summary_title = tk.Label(
    summary_card,
    text="Facture",
    font=("Arial", 14, "bold"),
    bg="white",
    fg="#1D5E42"
)

summary_title.pack(anchor="w")

summary_subtitle = tk.Label(
    summary_card,
    text="Résumé",
    font=("Arial", 12, "bold"),
    bg="white",
    fg="#4F6959"
)

summary_subtitle.pack(anchor="w", pady=(4, 8))

items_frame = tk.Frame(
    summary_card,
    bg="#F7FBF9",
    padx=10,
    pady=10
)
items_frame.pack(fill=tk.BOTH, expand=True)

liste = tk.Listbox(
    items_frame,
    bg="#F7FBF9",
    bd=0,
    highlightthickness=0,
    font=("Arial", 12),
    activestyle="none",
    selectbackground="#D7EADC",
    relief="flat"
)

liste.pack(fill=tk.BOTH, expand=True)

empty_label = tk.Label(
    items_frame,
    text="Aucun produit détecté. Scannez un UID.",
    bg="#F7FBF9",
    fg="#7A8C7D",
    font=("Arial", 12),
    justify="center"
)
empty_label.place(relx=0.5, rely=0.5, anchor="center")

footer_frame = tk.Frame(
    fenetre,
    bg="#E6F4EF",
    padx=16,
    pady=10
)
footer_frame.pack(fill=tk.X)

total_label = tk.Label(
    footer_frame,
    text="TOTAL : 0 FCFA",
    font=("Arial", 20, "bold"),
    bg="#E6F4EF",
    fg="#1E8F5D"
)

total_label.pack(pady=(0, 14))

button_frame = tk.Frame(
    footer_frame,
    bg="#E6F4EF"
)
button_frame.pack(fill=tk.X)

btn_payer = tk.Button(
    button_frame,
    text="PAYER",
    bg="#1E8F5D",
    fg="white",
    activebackground="#176a43",
    activeforeground="white",
    font=("Arial", 12, "bold"),
    bd=0,
    relief="flat",
    height=2,
    command=payer
)

btn_payer.pack(fill=tk.X, pady=(0, 8))

btn_vider = tk.Button(
    button_frame,
    text="RÉINITIALISER",
    bg="#FFFFFF",
    fg="#1E8F5D",
    activebackground="#E6F4EF",
    activeforeground="#1E8F5D",
    font=("Arial", 12, "bold"),
    bd=1,
    relief="solid",
    height=2,
    command=vider_panier
)

btn_vider.pack(fill=tk.X)

# ==========================
# THREAD RFID
# ==========================

def start_rfid_thread() -> None:
    threading.Thread(
        target=lecture_rfid,
        daemon=True
    ).start()

# ==========================
# LANCEMENT
# ==========================

def main() -> None:
    start_rfid_thread()
    try:
        fenetre.mainloop()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()