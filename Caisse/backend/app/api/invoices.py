import uuid
import logging
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models.product import Product
from app.models.invoice import Invoice, InvoiceItem
from app.models.security_log import SecurityLog
from app.schemas.invoice import InvoiceCreate, InvoiceResponse, InvoiceItemResponse, InvoiceListResponse, PaymentUpdate
from app.services.pdf_service import generate_receipt_pdf
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/", response_model=InvoiceResponse)
async def create_invoice(invoice_data: InvoiceCreate, db: AsyncSession = Depends(get_db)):
    """Create a new invoice from the detected cart items."""
    subtotal = 0
    invoice_items = []

    for item in invoice_data.items:
        # Verify product exists
        result = await db.execute(select(Product).where(Product.id == item.product_id))
        product = result.scalar_one_or_none()
        if not product:
            raise HTTPException(status_code=404, detail=f"Produit {item.product_id} non trouvé")

        item_total = item.quantity * item.unit_price
        subtotal += item_total

        invoice_items.append({
            "product_id": item.product_id,
            "quantity": item.quantity,
            "unit_price": item.unit_price,
            "product_name": product.name
        })

    # Calculate tax and total
    tax_amount = round(subtotal * settings.TAX_RATE, 2)
    total_amount = round(subtotal + tax_amount, 2)

    # Create invoice
    invoice = Invoice(
        subtotal=subtotal,
        tax_amount=tax_amount,
        total_amount=total_amount,
        payment_method=invoice_data.payment_method,
        payment_status="en_attente"
    )
    db.add(invoice)
    await db.flush()

    # Create invoice items
    for item_data in invoice_items:
        db_item = InvoiceItem(
            invoice_id=invoice.id,
            product_id=item_data["product_id"],
            quantity=item_data["quantity"],
            unit_price=item_data["unit_price"]
        )
        db.add(db_item)

    await db.commit()
    await db.refresh(invoice)

    # Generate PDF
    pdf_items = [
        {
            "name": it["product_name"],
            "quantity": it["quantity"],
            "unit_price": it["unit_price"]
        }
        for it in invoice_items
    ]

    generate_receipt_pdf(
        invoice_id=str(invoice.id),
        items=pdf_items,
        subtotal=subtotal,
        tax_amount=tax_amount,
        total_amount=total_amount,
        payment_method=invoice_data.payment_method,
        payment_status="en_attente"
    )

    # Build response
    items_response = []
    for it in invoice_items:
        items_response.append(InvoiceItemResponse(
            id=0,
            product_id=it["product_id"],
            product_name=it["product_name"],
            quantity=it["quantity"],
            unit_price=it["unit_price"],
            total=it["quantity"] * it["unit_price"]
        ))

    return InvoiceResponse(
        id=invoice.id,
        total_amount=total_amount,
        tax_amount=tax_amount,
        subtotal=subtotal,
        payment_status=invoice.payment_status,
        payment_method=invoice.payment_method,
        transaction_date=invoice.transaction_date,
        items=items_response
    )


@router.get("/", response_model=InvoiceListResponse)
async def list_invoices(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    count_result = await db.execute(select(func.count(Invoice.id)))
    total = count_result.scalar()

    result = await db.execute(
        select(Invoice).order_by(Invoice.transaction_date.desc()).offset(skip).limit(limit)
    )
    invoices = result.scalars().all()

    invoice_list = []
    for inv in invoices:
        # Get items
        items_result = await db.execute(
            select(InvoiceItem).where(InvoiceItem.invoice_id == inv.id)
        )
        items = items_result.scalars().all()

        items_resp = []
        for it in items:
            # Get product name
            prod_result = await db.execute(select(Product).where(Product.id == it.product_id))
            prod = prod_result.scalar_one_or_none()
            items_resp.append(InvoiceItemResponse(
                id=it.id,
                product_id=it.product_id,
                product_name=prod.name if prod else "Inconnu",
                quantity=it.quantity,
                unit_price=it.unit_price,
                total=it.quantity * it.unit_price
            ))

        invoice_list.append(InvoiceResponse(
            id=inv.id,
            total_amount=inv.total_amount,
            tax_amount=inv.tax_amount,
            subtotal=inv.subtotal,
            payment_status=inv.payment_status,
            payment_method=inv.payment_method,
            transaction_date=inv.transaction_date,
            items=items_resp
        ))

    return InvoiceListResponse(invoices=invoice_list, total=total)


@router.get("/{invoice_id}", response_model=InvoiceResponse)
async def get_invoice(invoice_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Facture non trouvée")

    items_result = await db.execute(
        select(InvoiceItem).where(InvoiceItem.invoice_id == invoice.id)
    )
    items = items_result.scalars().all()

    items_resp = []
    for it in items:
        prod_result = await db.execute(select(Product).where(Product.id == it.product_id))
        prod = prod_result.scalar_one_or_none()
        items_resp.append(InvoiceItemResponse(
            id=it.id,
            product_id=it.product_id,
            product_name=prod.name if prod else "Inconnu",
            quantity=it.quantity,
            unit_price=it.unit_price,
            total=it.quantity * it.unit_price
        ))

    return InvoiceResponse(
        id=invoice.id,
        total_amount=invoice.total_amount,
        tax_amount=invoice.tax_amount,
        subtotal=invoice.subtotal,
        payment_status=invoice.payment_status,
        payment_method=invoice.payment_method,
        transaction_date=invoice.transaction_date,
        items=items_resp
    )


@router.patch("/{invoice_id}/payment")
async def update_payment(
    invoice_id: uuid.UUID,
    payment: PaymentUpdate,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Facture non trouvée")

    invoice.payment_status = payment.payment_status
    if payment.payment_method:
        invoice.payment_method = payment.payment_method

    await db.commit()
    return {"message": "Paiement mis à jour", "status": payment.payment_status}


@router.get("/{invoice_id}/pdf")
async def download_invoice_pdf(invoice_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Invoice).where(Invoice.id == invoice_id))
    invoice = result.scalar_one_or_none()
    if not invoice:
        raise HTTPException(status_code=404, detail="Facture non trouvée")

    import os
    pdf_path = os.path.join(settings.UPLOAD_DIR, "invoices", f"{invoice_id}.pdf")

    if not os.path.exists(pdf_path):
        # Regenerate PDF
        items_result = await db.execute(
            select(InvoiceItem).where(InvoiceItem.invoice_id == invoice.id)
        )
        items = items_result.scalars().all()

        pdf_items = []
        for it in items:
            prod_result = await db.execute(select(Product).where(Product.id == it.product_id))
            prod = prod_result.scalar_one_or_none()
            pdf_items.append({
                "name": prod.name if prod else "Inconnu",
                "quantity": it.quantity,
                "unit_price": it.unit_price
            })

        pdf_path = generate_receipt_pdf(
            invoice_id=str(invoice.id),
            items=pdf_items,
            subtotal=invoice.subtotal,
            tax_amount=invoice.tax_amount,
            total_amount=invoice.total_amount,
            payment_method=invoice.payment_method or "Espèces",
            payment_status=invoice.payment_status
        )

    return FileResponse(
        pdf_path,
        media_type="application/pdf",
        filename=f"automaticCHECK_Facture_{str(invoice_id)[:8]}.pdf"
    )
