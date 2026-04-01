from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from uuid import UUID


class ProductCreate(BaseModel):
    name: str
    price: float
    category: Optional[str] = None
    stock_quantity: int = 0


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    stock_quantity: Optional[int] = None


class ProductResponse(BaseModel):
    id: UUID
    name: str
    price: float
    category: Optional[str]
    stock_quantity: int
    image_url: Optional[str]
    created_at: datetime
    embedding_count: int = 0

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    products: list[ProductResponse]
    total: int


class EmbeddingResponse(BaseModel):
    id: int
    product_id: UUID
    image_path: Optional[str]
    view_angle: Optional[str]

    class Config:
        from_attributes = True


class DetectionResult(BaseModel):
    product_name: str
    product_id: Optional[str] = None
    confidence: float
    price: float
    bbox: list[float]
