import os
import uuid
import logging
from typing import List

import cv2
import numpy as np
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models.product import Product, ProductEmbedding
from app.models.user import AdminUser
from app.schemas.product import ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
from app.utils.security import get_current_user
from app.services.ai_service import ai_service
from app.config import settings

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/", response_model=ProductListResponse)
async def list_products(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    # Count total
    count_result = await db.execute(select(func.count(Product.id)))
    total = count_result.scalar()

    # Get products with embedding count
    result = await db.execute(
        select(Product).order_by(Product.created_at.desc()).offset(skip).limit(limit)
    )
    products = result.scalars().all()

    product_list = []
    for p in products:
        # Count embeddings
        emb_result = await db.execute(
            select(func.count(ProductEmbedding.id)).where(ProductEmbedding.product_id == p.id)
        )
        emb_count = emb_result.scalar()

        product_list.append(ProductResponse(
            id=p.id,
            name=p.name,
            price=p.price,
            category=p.category,
            stock_quantity=p.stock_quantity,
            image_url=p.image_url,
            created_at=p.created_at,
            embedding_count=emb_count
        ))

    return ProductListResponse(products=product_list, total=total)


@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(product_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    emb_result = await db.execute(
        select(func.count(ProductEmbedding.id)).where(ProductEmbedding.product_id == product.id)
    )
    emb_count = emb_result.scalar()

    return ProductResponse(
        id=product.id,
        name=product.name,
        price=product.price,
        category=product.category,
        stock_quantity=product.stock_quantity,
        image_url=product.image_url,
        created_at=product.created_at,
        embedding_count=emb_count
    )


@router.post("/", response_model=ProductResponse)
async def create_product(
    product_data: ProductCreate,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    product = Product(
        name=product_data.name,
        price=product_data.price,
        category=product_data.category,
        stock_quantity=product_data.stock_quantity
    )
    db.add(product)
    await db.commit()
    await db.refresh(product)

    return ProductResponse(
        id=product.id,
        name=product.name,
        price=product.price,
        category=product.category,
        stock_quantity=product.stock_quantity,
        image_url=product.image_url,
        created_at=product.created_at,
        embedding_count=0
    )


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: uuid.UUID,
    product_data: ProductUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    update_fields = product_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(product, field, value)

    await db.commit()
    await db.refresh(product)

    emb_result = await db.execute(
        select(func.count(ProductEmbedding.id)).where(ProductEmbedding.product_id == product.id)
    )
    emb_count = emb_result.scalar()

    return ProductResponse(
        id=product.id,
        name=product.name,
        price=product.price,
        category=product.category,
        stock_quantity=product.stock_quantity,
        image_url=product.image_url,
        created_at=product.created_at,
        embedding_count=emb_count
    )


@router.delete("/{product_id}")
async def delete_product(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    await db.delete(product)
    await db.commit()
    return {"message": "Produit supprimé avec succès"}


@router.post("/{product_id}/train")
async def train_product(
    product_id: uuid.UUID,
    images: List[UploadFile] = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: AdminUser = Depends(get_current_user)
):
    """Upload up to 5 images for few-shot learning. Generates embeddings for product identification."""
    result = await db.execute(select(Product).where(Product.id == product_id))
    product = result.scalar_one_or_none()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")

    if len(images) > 5:
        raise HTTPException(status_code=400, detail="Maximum 5 images autorisées")

    # Create product upload directory
    product_dir = os.path.join(settings.UPLOAD_DIR, "products", str(product_id))
    os.makedirs(product_dir, exist_ok=True)

    view_angles = ["face", "dessus", "gauche", "droite", "arriere"]
    embeddings_created = 0
    first_image_path = None

    for i, image_file in enumerate(images):
        # Read image
        contents = await image_file.read()
        nparr = np.frombuffer(contents, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            logger.warning(f"Could not decode image {image_file.filename}")
            continue

        # Save original image
        ext = os.path.splitext(image_file.filename)[1] or ".jpg"
        img_filename = f"{view_angles[i] if i < len(view_angles) else f'view_{i}'}{ext}"
        img_path = os.path.join(product_dir, img_filename)
        cv2.imwrite(img_path, img)

        if first_image_path is None:
            first_image_path = f"/uploads/products/{product_id}/{img_filename}"

        # Process and extract embedding
        embedding, crop = ai_service.process_training_image(img)

        # Save crop
        crop_path = os.path.join(product_dir, f"crop_{img_filename}")
        cv2.imwrite(crop_path, crop)

        # Store embedding in database
        db_embedding = ProductEmbedding(
            product_id=product_id,
            embedding=embedding,
            image_path=f"/uploads/products/{product_id}/{img_filename}",
            view_angle=view_angles[i] if i < len(view_angles) else f"view_{i}"
        )
        db.add(db_embedding)
        embeddings_created += 1

    # Update product image_url with first image
    if first_image_path:
        product.image_url = first_image_path

    await db.commit()

    return {
        "message": f"{embeddings_created} embeddings créés avec succès pour '{product.name}'",
        "product_id": str(product_id),
        "embeddings_created": embeddings_created
    }


@router.get("/{product_id}/embeddings")
async def get_product_embeddings(
    product_id: uuid.UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(ProductEmbedding).where(ProductEmbedding.product_id == product_id)
    )
    embeddings = result.scalars().all()

    return {
        "product_id": str(product_id),
        "count": len(embeddings),
        "embeddings": [
            {
                "id": e.id,
                "image_path": e.image_path,
                "view_angle": e.view_angle
            }
            for e in embeddings
        ]
    }
