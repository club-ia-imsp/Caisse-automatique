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

def generer_recu_ets(liste_produits, client, caissier):
    num_recu = gerer_compteur()
    nom_fichier = f"Recu_{num_recu}.pdf"
    date_str = datetime.now().strftime("%d/%m/%Y")
    heure_str = datetime.now().strftime("%H:%M:%S")
    
    c = canvas.Canvas(nom_fichier, pagesize=A6)
    width, height = A6
    bleu_noir = colors.Color(0.05, 0.1, 0.25)

    # --- 1. EN-TÊTE ---
    c.setFont("Helvetica-Bold", 11)
    c.setFillColor(bleu_noir)
    c.drawString(10*mm, height - 10*mm, "Ets Caisse Automatique")
    
    c.setFont("Helvetica-Bold", 7)
    c.drawRightString(100*mm, height - 10*mm, f"DATE : {date_str} à {heure_str}")
    c.drawRightString(100*mm, height - 15*mm, f"REÇU NO : {num_recu}")

    # --- 2. IDENTITÉ (Soulignée) ---
    y_id = height - 28*mm
    c.setFont("Helvetica-Bold", 8)
    
    # Client
    txt_client = f"Client : {client if client else '................'}"
    c.drawString(10*mm, y_id, txt_client)
    c.line(10*mm, y_id - 1*mm, 10*mm + c.stringWidth(txt_client, "Helvetica-Bold", 8), y_id - 1*mm)
    
    # Caissier
    txt_caissier = f"Caissier : {caissier if caissier else '................'}"
    c.drawString(60*mm, y_id, txt_caissier)
    c.line(60*mm, y_id - 1*mm, 60*mm + c.stringWidth(txt_caissier, "Helvetica-Bold", 8), y_id - 1*mm)

    # --- 3. TABLEAU ---
    data = [['Description', 'P. Unit', 'Qté', 'Montant']]
    total_general = 0
    total_articles = 0

    for p in liste_produits:
        montant_ligne = p['prix'] * p['qte']
        data.append([p['nom'], f"{p['prix']}", str(p['qte']), f"{montant_ligne}"])
        total_general += montant_ligne
        total_articles += p['qte']

    while len(data) < 10:
        data.append(['', '', '', ''])

    table = Table(data, colWidths=[40*mm, 20*mm, 10*mm, 20*mm], rowHeights=5*mm)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), bleu_noir),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, bleu_noir),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
    ]))
    
    table.wrapOn(c, width, height)
    y_table = y_id - 55*mm 
    table.drawOn(c, 10*mm, y_table)

    # --- 4. TOTAUX À GAUCHE (Soulignés, sans cadre) ---
    y_totaux = y_table - 12*mm 
    
    # Nombre d'articles
    c.setFont("Helvetica-Bold", 8)
    txt_nb = f"NOMBRE TOTAL D'ARTICLES : {total_articles}"
    c.drawString(10*mm, y_totaux + 6*mm, txt_nb)
    c.line(10*mm, y_totaux + 5*mm, 10*mm + c.stringWidth(txt_nb, "Helvetica-Bold", 8), y_totaux + 5*mm)
    
    # Prix Total (plus grand et gras)
    c.setFont("Helvetica-Bold", 10)
    txt_total = f"TOTAL À PAYER : {total_general} CFA"
    c.drawString(10*mm, y_totaux - 2*mm, txt_total)
    # Ligne de soulignement plus épaisse pour le montant final
    c.setLineWidth(1.2) 
    c.line(10*mm, y_totaux - 3.5*mm, 10*mm + c.stringWidth(txt_total, "Helvetica-Bold", 10), y_totaux - 3.5*mm)
    c.setLineWidth(1) # Retour à la normale

    # --- 5. SIGNATURES ---
    y_sign = 20*mm
    c.setFont("Helvetica-Bold", 7)
    
    c.line(10*mm, y_sign, 45*mm, y_sign)
    c.drawCentredString(27.5*mm, y_sign - 4*mm, "SIGNATURE CLIENT")
    
    c.line(65*mm, y_sign, 100*mm, y_sign)
    c.drawCentredString(82.5*mm, y_sign - 4*mm, "SIGNATURE CAISSIER")

    c.save()
    print(f"\n✅ REÇU GÉNÉRÉ AVEC TOTAUX SOULIGNÉS : {nom_fichier}")

# --- INTERFACE ---
if __name__ == "__main__":
    cl = input("Client : ")
    ca = "Caissier" 
    
    items = []
    while True:
        nom = input("\nArticle (ou 'fin') : ")
        if nom.lower() == 'fin': break
        try:
            p = float(input("Prix : "))
            q = int(input("Qté : "))
            items.append({'nom': nom, 'prix': p, 'qte': q})
        except:
            print("Erreur de saisie.")

    generer_recu_ets(items, cl, ca)
    