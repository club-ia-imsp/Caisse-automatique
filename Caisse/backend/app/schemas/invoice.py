from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class InvoiceItemCreate(BaseModel):
    product_id: UUID
    quantity: int
    unit_price: float


class InvoiceCreate(BaseModel):
    items: list[InvoiceItemCreate]
    payment_method: str = "especes"


class InvoiceItemResponse(BaseModel):
    id: int
    product_id: UUID
    product_name: Optional[str] = None
    quantity: int
    unit_price: float
    total: float = 0

    class Config:
        from_attributes = True


class InvoiceResponse(BaseModel):
    id: UUID
    total_amount: float
    tax_amount: float
    subtotal: float
    payment_status: str
    payment_method: Optional[str]
    transaction_date: datetime
    items: list[InvoiceItemResponse] = []

    class Config:
        from_attributes = True


class InvoiceListResponse(BaseModel):
    invoices: list[InvoiceResponse]
    total: int


class PaymentUpdate(BaseModel):
    payment_status: str
    payment_method: Optional[str] = None
