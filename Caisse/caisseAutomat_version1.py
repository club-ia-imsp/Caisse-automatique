import sys
import os
import time
import random
import string
import cv2
import numpy as np
import pandas as pd
from datetime import datetime
from collections import Counter
from ultralytics import YOLO
from fpdf import FPDF
from fpdf.enums import XPos, YPos
import fitz  # PyMuPDF

from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QDialog, QScrollArea
from PyQt5.QtGui import QImage, QPixmap, QFont, QCursor
from PyQt5.QtCore import QTimer, Qt


model = YOLO('best_caisse.pt')        # Modèle YOLO
dict_ = {0: 'assiette', 1: 'banane', 2: 'bouteille', 3: 'couteau', 4: 'cuillere', 5: 'fourchette',
         6: 'livre', 7: 'oeuf', 8: 'pomme', 9: 'stylo'}


prix_articles = [
    {'nom': 'assiette', 'prix': 2.50, 'emoji': '🍽️'},
    {'nom': 'banane', 'prix': 1.20, 'emoji': '🍌'},
    {'nom': 'bouteille', 'prix': 1.50, 'emoji': '🍾'},
    {'nom': 'couteau', 'prix': 3.00, 'emoji': '🔪'},
    {'nom': 'cuillere', 'prix': 1.80, 'emoji': '🥄'},
    {'nom': 'fourchette', 'prix': 1.80, 'emoji': '🍴'},
    {'nom': 'livre', 'prix': 8.00, 'emoji': '📚'},
    {'nom': 'oeuf', 'prix': 0.80, 'emoji': '🥚'},
    {'nom': 'pomme', 'prix': 1.00, 'emoji': '🍎'},
    {'nom': 'stylo', 'prix': 2.00, 'emoji': '🖊️'}
]


def capture_image(cap):
    """Capturer une image depuis la caméra déjà ouverte"""
    if cap is None or not cap.isOpened():
        return None
    ret, frame = cap.read()  
    if not ret:
        return None
    return frame




def yolo_inference(image):
    results = model(image)
    return results[0].plot(), results




def tableur(articles: list):
    element = list(set(articles))
    dicta = [(article, articles.count(article)) for article in element]
    df = pd.DataFrame(dicta, columns=["Articles", "Nombre"])


    prices_dict = {item['nom']: item['prix'] for item in prix_articles}
    df['Prix'] = df['Articles'].map(prices_dict)


    articles_with_prices = []
    for _, row in df.iterrows():
        articles_with_prices.append({
            'nom': row['Articles'],
            'prix': row['Prix'],
            'quantite': row['Nombre']
        })
    return articles_with_prices




def facture(article_liste):
    df = pd.DataFrame(article_liste)
    df['total'] = df['prix'] * df['quantite']
    return df




def generate_code():
    return 'FCT-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))




def generate_pdf(facture_df, code, background_path=None):
    pdf = FPDF()
    pdf.add_page()
    #Ajouter l'image de fond si elle existe 
    if background_path and os.path.exists(background_path):
        pdf.image(background_path, x=0, y=0, w=210, h=297)  # A4 : 210x297 mm


    #En-tête
    pdf.set_font("Helvetica", 'B', 16)
    pdf.cell(200, 10, "Caisse Automatique", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(5)


    # Date et heure
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    pdf.set_font("helvetica", '', 10)
    pdf.cell(200, 10, f"Date : {now}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(5)


    #Numéro de facture
    pdf.set_font("Helvetica", 'B', 12)
    pdf.cell(200, 10, text=f"Facture N°: {code}", align='C')
    pdf.ln(15)




    pdf.set_font("helvetica", 'B', 12)
    pdf.cell(65, 10, "Articles_detect", border=1, align='C', new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(40, 10, "Quantité", border=1, align='C', new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(40, 10, "Prix", border=1, align='C', new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(40, 10, "Total", border=1, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    
    pdf.set_font("helvetica", '', 12)
    for _, row in facture_df.iterrows():
        pdf.cell(65, 10, row['nom'], border=1, align='C', new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(40, 10, str(row['quantite']), border=1, align='C', new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(40, 10, f"{row['prix']:.2f}", border=1, align='C', new_x=XPos.RIGHT, new_y=YPos.TOP)
        pdf.cell(40, 10, f"{row['total']:.2f}", border=1, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)
# Total général
    total_general = facture_df['total'].sum()
    pdf.set_font("helvetica", 'B', 12)
    pdf.cell(145, 10, "Total à payer", border=1, align='C', new_x=XPos.RIGHT, new_y=YPos.TOP)
    pdf.cell(40, 10, f"{total_general:.2f} FCFA", border=1, align='C', new_x=XPos.LMARGIN, new_y=YPos.NEXT)


    folder_path = 'factures'
    os.makedirs(folder_path, exist_ok=True)
    pdf_path = os.path.join(folder_path, f"{code}.pdf")
    pdf.output(pdf_path)


    return pdf_path




def pdf_to_image(pdf_path):
    """Convertir toutes les pages du PDF généré en images pour affichage."""


    doc = fitz.open(pdf_path)
    images = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        pix = page.get_pixmap()
        
        if pix.n == 4:  # BGRA
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 4)
            img=cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        else:  # RGB
            img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, 3)
        
        images.append(img)
        
    return images
    


# ===============================
# FENÊTRE D'AGRANDISSEMENT
# ===============================
class FactureViewDialog(QDialog):
    def __init__(self, pixmap, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Facture - Aperçu complet")
        self.setModal(False)
        
        # Taille de la fenêtre
        screen = QApplication.primaryScreen().geometry()
        dialog_width = min(800, screen.width() - 100)
        dialog_height = min(1000, screen.height() - 100)
        self.setGeometry(100, 50, dialog_width, dialog_height)
        
        # Style
        self.setStyleSheet("background-color: #2c3e50;")
        
        # Layout principal
        layout = QVBoxLayout()
        
        # Zone scrollable
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background-color: #34495e; border: none;")
        
        # Label pour l'image
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignCenter)
        image_label.setPixmap(pixmap)
        image_label.setScaledContents(False)
        
        scroll.setWidget(image_label)
        layout.addWidget(scroll)
        
        # Bouton de fermeture
        close_btn = QPushButton("Fermer")
        close_btn.setStyleSheet("""
            background-color: #e74c3c;
            color: white;
            font-weight: bold;
            font-size: 14px;
            padding: 10px;
            border-radius: 5px;
        """)
        close_btn.clicked.connect(self.close)
        layout.addWidget(close_btn)
        
        self.setLayout(layout)


# ===============================
# LABEL CLIQUABLE POUR FACTURE
# ===============================
class ClickableLabel(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.full_pixmap = None
        self.setCursor(QCursor(Qt.PointingHandCursor))
    
    def mousePressEvent(self, event):
        if self.full_pixmap and not self.full_pixmap.isNull():
            dialog = FactureViewDialog(self.full_pixmap, self)
            dialog.exec_()
        super().mousePressEvent(event)
    
    def setFullPixmap(self, pixmap):
        """Stocker le pixmap original en taille réelle"""
        self.full_pixmap = pixmap


# ===============================
# INTERFACE
# ===============================
class Interface(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caisse Automatique - Détection en temps réel")
        self.setGeometry(100, 100, 1400, 700)

        # Style moderne
        self.setStyleSheet("background-color: #f0f2f5;")

        # Variables
        self.cap = None
        self.cart = {}  # Panier avec quantités détectées

        # Layout principal vertical
        vbox = QVBoxLayout()

        # Titre
        title = QLabel("🛒 Caisse Automatique - Détection Intelligente")
        title.setFont(QFont('Arial', 24, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #2c3e50; margin: 15px; padding: 10px;")
        vbox.addWidget(title)

        # Zone centrale avec trois sections
        hbox = QHBoxLayout()
        
        # 1. Flux caméra
        cam_vbox = QVBoxLayout()
        cam_label = QLabel("📹Détection en Direct")
        cam_label.setFont(QFont('Arial', 16, QFont.Bold))
        cam_label.setStyleSheet("color: #34495e; margin: 5px;")
        cam_vbox.addWidget(cam_label)
        
        self.label_detection = QLabel("Activez la caméra pour commencer")
        self.label_detection.setAlignment(Qt.AlignCenter)
        self.label_detection.setMinimumSize(500, 400)
        self.label_detection.setStyleSheet("""
            background-color: #2c3e50; 
            color: white; 
            font-size: 16px;
            border-radius: 10px;
            padding: 20px;
        """)
        cam_vbox.addWidget(self.label_detection)
        hbox.addLayout(cam_vbox)

        # 2. Panier détecté
        cart_vbox = QVBoxLayout()
        cart_label = QLabel("🛒Panier Détecté")
        cart_label.setFont(QFont('Arial', 16, QFont.Bold))
        cart_label.setStyleSheet("color: #34495e; margin: 5px;")
        cart_vbox.addWidget(cart_label)
        
        self.label_cart = QLabel("Aucun article détecté")
        self.label_cart.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.label_cart.setMinimumSize(300, 400)
        self.label_cart.setStyleSheet("""
            background-color: white; 
            color: #2c3e50; 
            font-size: 14px;
            border: 2px solid #bdc3c7;
            border-radius: 10px;
            padding: 15px;
        """)
        self.label_cart.setWordWrap(True)
        cart_vbox.addWidget(self.label_cart)
        hbox.addLayout(cart_vbox)

        # 3. Facture générée
        facture_vbox = QVBoxLayout()
        facture_label = QLabel("Facture")
        facture_label.setFont(QFont('Arial', 16, QFont.Bold))
        facture_label.setStyleSheet("color: #34495e; margin: 5px;")
        facture_vbox.addWidget(facture_label)
        
        self.label_facture = ClickableLabel("Générez une facture")
        self.label_facture.setAlignment(Qt.AlignCenter)
        self.label_facture.setMinimumSize(400, 400)
        self.label_facture.setStyleSheet("""
            background-color: #ecf0f1; 
            color: #7f8c8d; 
            font-size: 14px;
            border: 2px dashed #95a5a6;
            border-radius: 10px;
            padding: 10px;
        """)
        facture_vbox.addWidget(self.label_facture)
        hbox.addLayout(facture_vbox)

        vbox.addLayout(hbox)

        # Boutons de contrôle
        control_box = QHBoxLayout()
        
        self.start_button = QPushButton("Démarrer")
        self.start_button.setStyleSheet("""
            background-color: #27ae60; 
            color: white; 
            font-weight: bold; 
            font-size: 16px; 
            padding: 15px;
            border-radius: 8px;
        """)
        self.start_button.clicked.connect(self.start_process)
        control_box.addWidget(self.start_button)

        self.invoice_button = QPushButton("Générer Facture")
        self.invoice_button.setStyleSheet("""
            background-color: #3498db; 
            color: white; 
            font-weight: bold; 
            font-size: 16px; 
            padding: 15px;
            border-radius: 8px;
        """)
        self.invoice_button.clicked.connect(self.generate_invoice)
        self.invoice_button.setEnabled(False)
        control_box.addWidget(self.invoice_button)

        self.stop_button = QPushButton("Arrêter")
        self.stop_button.setStyleSheet("""
            background-color: #e74c3c; 
            color: white; 
            font-weight: bold; 
            font-size: 16px; 
            padding: 15px;
            border-radius: 8px;
        """)
        self.stop_button.clicked.connect(self.stop_process)
        self.stop_button.setEnabled(False)
        control_box.addWidget(self.stop_button)

        vbox.addLayout(control_box)

        self.setLayout(vbox)

        # Timer pour mise à jour
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frames)

    def start_process(self):
        """Démarrer la détection"""
        if not self.timer.isActive():
            # Ouvrir la caméra
            self.cap = cv2.VideoCapture(1)
            if not self.cap.isOpened():
                self.cap = cv2.VideoCapture(0)
            
            if self.cap.isOpened():
                self.timer.start(100)  # toutes les 100 ms
                self.start_button.setEnabled(False)
                self.stop_button.setEnabled(True)
                self.invoice_button.setEnabled(True)
            else:
                self.label_detection.setText("Impossible d'ouvrir la caméra")

    def stop_process(self):
        """Arrêter la détection"""
        if self.timer.isActive():
            self.timer.stop()
            
        if self.cap:
            self.cap.release()
            self.cap = None
            
        self.label_detection.setText("Caméra arrêtée")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.invoice_button.setEnabled(False)
        self.cart = {}
        self.update_cart_display()

    def update_cart_display(self):
        """Mettre à jour l'affichage du panier"""
        if not self.cart:
            self.label_cart.setText("Aucun article détecté")
            return
        
        cart_text = "<h3 style='color: #2c3e50; margin-bottom: 10px;'>Articles détectés:</h3>"
        total = 0
        
        for name, data in self.cart.items():
            emoji = data.get('emoji', '📦')
            subtotal = data['prix'] * data['quantite']
            total += subtotal
            cart_text += f"""
                <div style='margin: 8px 0; padding: 8px; background: #ecf0f1; border-radius: 5px;'>
                    <b>{emoji} {name.capitalize()}</b><br>
                    <span style='color: #7f8c8d;'>
                        {data['prix']:.2f} FCFA × {data['quantite']} = {subtotal:.2f} FCFA
                    </span>
                </div>
            """
        
        cart_text += f"<hr><h3 style='color: #27ae60;'>Total: {total:.2f} FCFA</h3>"
        self.label_cart.setText(cart_text)
    
    def update_frames(self):
        """Mettre à jour le flux caméra et détecter"""
        image = capture_image(self.cap)
        if image is None:
            return

        detection_frame, results = yolo_inference(image)

        # Affichage YOLO
        rgb_image = cv2.cvtColor(detection_frame, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        qt_image = QImage(rgb_image.data, w, h, ch * w, QImage.Format_RGB888)
        self.label_detection.setPixmap(QPixmap.fromImage(qt_image).scaled(
            self.label_detection.width(), self.label_detection.height(), Qt.KeepAspectRatio
        ))

        # Mettre à jour le panier
        articles = [dict_[int(i)] for i in results[0].boxes.cls]
        
        if articles:
            # Compter les articles détectés
            article_counts = Counter(articles)
            
            # Mettre à jour le panier avec les quantités exactes
            self.cart = {}
            for article, count in article_counts.items():
                product = next((p for p in prix_articles if p['nom'] == article), None)
                if product:
                    self.cart[article] = {
                        'prix': product['prix'],
                        'quantite': count,
                        'emoji': product.get('emoji', '📦')
                    }
            
            self.update_cart_display()
        else:
            self.cart = {}
            self.update_cart_display()

    def generate_invoice(self):
        """Générer la facture PDF"""
        if not self.cart:
            self.label_facture.setText("Panier vide !")
            return
        
        # Créer la liste d'articles pour la facture
        articles_list = []
        for name, data in self.cart.items():
            articles_list.append({
                'nom': name,
                'prix': data['prix'],
                'quantite': data['quantite']
            })
        
        # Générer le PDF
        facture_df = facture(articles_list)
        code = generate_code()
        pdf_path = generate_pdf(facture_df, code)

        # Afficher l'aperçu
        facture_imgs = pdf_to_image(pdf_path)
        if facture_imgs:
            facture_img = facture_imgs[0]
            rgb_facture = cv2.cvtColor(facture_img, cv2.COLOR_BGR2RGB)
            h2, w2, ch2 = rgb_facture.shape
            qt_facture = QImage(rgb_facture.data, w2, h2, ch2 * w2, QImage.Format_RGB888)
            full_pixmap = QPixmap.fromImage(qt_facture)
            
            # Stocker l'image en taille réelle
            self.label_facture.setFullPixmap(full_pixmap)
            
            # Afficher une version réduite
            self.label_facture.setPixmap(full_pixmap.scaled(
                self.label_facture.width(), self.label_facture.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation
            ))
            
            self.label_facture.setStyleSheet("""
                background-color: white; 
                border: 2px solid #27ae60;
                border-radius: 10px;
                padding: 5px;
            """)
            self.label_facture.setToolTip("Cliquez pour agrandir")


# ===============================
# MAIN
# ===============================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Interface()
    win.show()
    sys.exit(app.exec_())
