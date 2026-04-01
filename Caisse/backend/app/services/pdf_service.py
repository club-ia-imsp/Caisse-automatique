"""
PDF Service - Generate supermarket-style receipt PDFs (80mm format)
"""

import os
from datetime import datetime
from fpdf import FPDF
from fpdf.enums import XPos, YPos


def generate_receipt_pdf(
    invoice_id: str,
    items: list,
    subtotal: float,
    tax_amount: float,
    total_amount: float,
    payment_method: str = "Espèces",
    payment_status: str = "Payé"
) -> str:
    """Generate a supermarket receipt PDF (80mm width)."""

    # 80mm width, dynamic height
    page_width = 80
    page_height = 200
    pdf = FPDF(format=(page_width, page_height))
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=5)

    w = page_width - 10  # usable width with 5mm margins
    pdf.set_left_margin(5)
    pdf.set_right_margin(5)

    # Header
    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(w, 6, "automaticCHECK", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(w, 4, "Caisse Automatique Intelligente", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(2)

    # Separator
    pdf.set_font("Courier", "", 7)
    pdf.cell(w, 3, "=" * 38, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(1)

    # Date and invoice number
    now = datetime.now().strftime("%d/%m/%Y  %H:%M:%S")
    pdf.set_font("Helvetica", "", 7)
    pdf.cell(w, 4, f"Date: {now}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
    pdf.cell(w, 4, f"Facture: {invoice_id[:13]}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
    pdf.ln(1)

    # Separator
    pdf.set_font("Courier", "", 7)
    pdf.cell(w, 3, "-" * 38, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(1)

    # Column headers
    pdf.set_font("Helvetica", "B", 7)
    col_w = [32, 8, 14, 16]
    pdf.cell(col_w[0], 4, "Article", new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")
    pdf.cell(col_w[1], 4, "Qte", new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")
    pdf.cell(col_w[2], 4, "P.U", new_x=XPos.RIGHT, new_y=YPos.TOP, align="R")
    pdf.cell(col_w[3], 4, "Total", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")

    pdf.set_font("Courier", "", 7)
    pdf.cell(w, 3, "-" * 38, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # Items
    pdf.set_font("Helvetica", "", 7)
    for item in items:
        name = item["name"][:18]
        qty = item["quantity"]
        price = item["unit_price"]
        total = qty * price
        pdf.cell(col_w[0], 4, name, new_x=XPos.RIGHT, new_y=YPos.TOP, align="L")
        pdf.cell(col_w[1], 4, f"x{qty}", new_x=XPos.RIGHT, new_y=YPos.TOP, align="C")
        pdf.cell(col_w[2], 4, f"{price:.0f}", new_x=XPos.RIGHT, new_y=YPos.TOP, align="R")
        pdf.cell(col_w[3], 4, f"{total:.0f}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")

    # Separator
    pdf.set_font("Courier", "", 7)
    pdf.cell(w, 3, "=" * 38, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.ln(1)

    # Totals
    total_label_w = w - 20
    total_val_w = 20

    pdf.set_font("Helvetica", "", 8)
    pdf.cell(total_label_w, 4, "Sous-total:", new_x=XPos.RIGHT, new_y=YPos.TOP, align="R")
    pdf.cell(total_val_w, 4, f"{subtotal:.0f} FCFA", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")

    pdf.cell(total_label_w, 4, "TVA (18%):", new_x=XPos.RIGHT, new_y=YPos.TOP, align="R")
    pdf.cell(total_val_w, 4, f"{tax_amount:.0f} FCFA", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")

    pdf.set_font("Courier", "", 7)
    pdf.cell(w, 3, "-" * 38, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    pdf.set_font("Helvetica", "B", 10)
    pdf.cell(total_label_w, 5, "TOTAL:", new_x=XPos.RIGHT, new_y=YPos.TOP, align="R")
    pdf.cell(total_val_w, 5, f"{total_amount:.0f} FCFA", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="R")
    pdf.ln(2)

    # Payment info
    pdf.set_font("Courier", "", 7)
    pdf.cell(w, 3, "-" * 38, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_font("Helvetica", "", 7)
    pdf.cell(w, 4, f"Paiement: {payment_method}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
    pdf.cell(w, 4, f"Statut: {payment_status}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="L")
    pdf.ln(2)

    # Footer
    pdf.set_font("Courier", "", 7)
    pdf.cell(w, 3, "=" * 38, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.set_font("Helvetica", "I", 7)
    pdf.cell(w, 4, "Merci de votre visite!", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
    pdf.cell(w, 4, "automaticCHECK - Caisse Intelligente", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")

    # Save
    folder_path = os.path.join(os.getenv("UPLOAD_DIR", "/app/uploads"), "invoices")
    os.makedirs(folder_path, exist_ok=True)
    pdf_path = os.path.join(folder_path, f"{invoice_id}.pdf")
    pdf.output(pdf_path)

    return pdf_path
