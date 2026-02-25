from reportlab.lib.pagesizes import A6
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from datetime import datetime
import os

def gerer_compteur():
    fichier = "compteur.txt"
    numero = 1
    if os.path.exists(fichier):
        with open(fichier, "r") as f:
            try:
                numero = int(f.read().strip()) + 1
            except:
                numero = 1
    with open(fichier, "w") as f:
        f.write(str(numero))
    return f"{numero:08d}"

def generer_recu_ets(liste_produits, client, caissier, logo_nom="logo.png"):
    num_recu = gerer_compteur()
    nom_fichier = f"Recu_{num_recu}.pdf"
    date_str = datetime.now().strftime("%d/%m/%Y")
    heure_str = datetime.now().strftime("%H:%M:%S")
    
    c = canvas.Canvas(nom_fichier, pagesize=A6)
    width, height = A6
    bleu_noir = colors.Color(0.05, 0.1, 0.25)

    # --- FILIGRANE (Watermark) ---
    # Le programme cherche le fichier logo_nom dans le dossier
    if os.path.exists(logo_nom):
        c.saveState()
        c.setFillAlpha(0.12) # Très léger
        c.drawImage(logo_nom, width/2 - 25*mm, height/2 - 20*mm, width=50*mm, preserveAspectRatio=True, mask='auto')
        c.restoreState()

    # --- 1. EN-TÊTE ---
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(bleu_noir)
    c.drawString(10*mm, height - 10*mm, "Ets Caisse Automatique")
    
    # Petit logo en haut à gauche sous le nom de l'entreprise
    if os.path.exists(logo_nom):
        c.drawImage(logo_nom, 10*mm, height - 22*mm, width=15*mm, preserveAspectRatio=True, mask='auto')

    c.setFont("Helvetica-Bold", 7)
    c.drawRightString(100*mm, height - 10*mm, f"DATE : {date_str} à {heure_str}")
    c.drawRightString(100*mm, height - 15*mm, f"REÇU NO : {num_recu}")

    # --- 2. IDENTITÉ SOULIGNÉE ---
    y_id = height - 32*mm
    c.setFont("Helvetica-Bold", 8)
    
    txt_cl = f"Client : {client if client else '................'}"
    c.drawString(10*mm, y_id, txt_cl)
    c.line(10*mm, y_id - 1*mm, 10*mm + c.stringWidth(txt_cl, "Helvetica-Bold", 8), y_id - 1*mm)
    
    txt_ca = f"Caissier : {caissier if caissier else '................'}"
    c.drawString(60*mm, y_id, txt_ca)
    c.line(60*mm, y_id - 1*mm, 60*mm + c.stringWidth(txt_ca, "Helvetica-Bold", 8), y_id - 1*mm)

    # --- 3. TABLEAU ---
    data = [['Description', 'P. Unit', 'Qté', 'Montant']]
    total_general = 0
    total_articles = 0
    for p in liste_produits:
        m = p['prix'] * p['qte']
        data.append([p['nom'], f"{p['prix']}", str(p['qte']), f"{m}"])
        total_general += m
        total_articles += p['qte']

    while len(data) < 10: data.append(['', '', '', ''])

    table = Table(data, colWidths=[40*mm, 20*mm, 10*mm, 20*mm], rowHeights=5*mm)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), bleu_noir),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, bleu_noir),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
    ]))
    table.wrapOn(c, width, height)
    y_tab = y_id - 55*mm
    table.drawOn(c, 10*mm, y_tab)

    # --- 4. TOTAUX SOULIGNÉS À GAUCHE ---
    y_tot = y_tab - 12*mm
    c.setFont("Helvetica-Bold", 8)
    t_nb = f"NOMBRE TOTAL D'ARTICLES : {total_articles}"
    c.drawString(10*mm, y_tot + 6*mm, t_nb)
    c.line(10*mm, y_tot + 5*mm, 10*mm + c.stringWidth(t_nb, "Helvetica-Bold", 8), y_tot + 5*mm)

    c.setFont("Helvetica-Bold", 10)
    t_pay = f"TOTAL À PAYER : {total_general} CFA"
    c.drawString(10*mm, y_tot - 2*mm, t_pay)
    c.setLineWidth(1.2)
    c.line(10*mm, y_tot - 3.5*mm, 10*mm + c.stringWidth(t_pay, "Helvetica-Bold", 10), y_tot - 3.5*mm)

    # --- 5. SIGNATURES ---
    y_sig = 18*mm
    c.setLineWidth(1)
    c.setFont("Helvetica-Bold", 7)
    c.line(10*mm, y_sig, 45*mm, y_sig)
    c.drawCentredString(27.5*mm, y_sig - 4*mm, "SIGNATURE CLIENT")
    c.line(65*mm, y_sig, 100*mm, y_sig)
    c.drawCentredString(82.5*mm, y_sig - 4*mm, "SIGNATURE CAISSIER")

    c.save()
    print(f"\n✅ Reçu généré avec filigrane : {nom_fichier}")

# --- LANCEMENT ---
if __name__ == "__main__":
    # ÉTAPE IMPORTANTE : Changez "mon_logo.png" par le vrai nom de votre image
    NOM_DU_LOGO = "logo.png" 
    
    client_nom = input("Client : ")
    caissier_nom = input("Caissier : ")
    
    panier = []
    while True:
        art = input("\nArticle (ou 'fin') : ")
        if art.lower() == 'fin': break
        try:
            pu = float(input("Prix : "))
            q = int(input("Qté : "))
            panier.append({'nom': art, 'prix': pu, 'qte': q})
        except: print("Erreur chiffre.")

    generer_recu_ets(panier, client_nom, caissier_nom, logo_nom=NOM_DU_LOGO)