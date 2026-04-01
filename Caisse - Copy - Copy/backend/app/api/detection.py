"""
WebSocket endpoint for real-time product detection.
Uses best_caisse.pt: YOLO detects objects and returns class names directly.
Class names are matched to products in DB by name — same approach as the PyQt5 app.
"""

import base64
import json
import logging
import asyncio

import cv2
import numpy as np
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import async_session
from app.models.product import Product
from app.services.ai_service import ai_service

logger = logging.getLogger(__name__)
router = APIRouter()


async def process_frame(image: np.ndarray) -> dict:
    """
    Process a single frame:
      1. YOLO (best_caisse.pt) detects objects → class names (e.g. 'banane', 'couteau')
      2. Class names matched to products in DB by name (case-insensitive)
      3. Returns annotated frame + cart
    Mirrors the PyQt5 caisseAutomat.py approach exactly.
    """
    loop = asyncio.get_running_loop()

    # Run YOLO detection in thread pool
    detections = await loop.run_in_executor(None, ai_service.detect_objects, image)

    if not detections:
        _, buffer = cv2.imencode('.jpg', image, [cv2.IMWRITE_JPEG_QUALITY, 80])
        return {"detections": [], "cart": {}, "annotated_frame": base64.b64encode(buffer).decode()}

    # Unique lowercase class names detected in this frame
    class_names = list({det["class_name"].lower() for det in detections})

    # Batch DB lookup: find products whose name matches a detected class name
    async with async_session() as db:
        result = await db.execute(
            select(Product).where(func.lower(Product.name).in_(class_names))
        )
        products_list = result.scalars().all()

    # Build fast lookup: lowercase_name → product row
    product_map = {p.name.lower(): p for p in products_list}

    # Enrich each detection with product info from DB
    identified_products = []
    for det in detections:
        name_lower = det["class_name"].lower()
        product = product_map.get(name_lower)
        if product:
            identified_products.append({
                "product_id": str(product.id),
                "product_name": product.name,
                "price": float(product.price),
                "confidence": det["confidence"],
                "bbox": det["bbox"]
            })
        else:
            # Class detected by YOLO but not in DB yet — show it but no price
            identified_products.append({
                "product_id": None,
                "product_name": det["class_name"],
                "price": 0,
                "confidence": det["confidence"],
                "bbox": det["bbox"]
            })

    # Build cart: aggregate quantities by product_id
    cart = {}
    for prod in identified_products:
        pid = prod["product_id"]
        if pid:
            if pid not in cart:
                cart[pid] = {
                    "product_id": pid,
                    "product_name": prod["product_name"],
                    "price": prod["price"],
                    "quantity": 0
                }
            cart[pid]["quantity"] += 1

    # Draw bounding boxes on the frame
    annotated = await loop.run_in_executor(None, ai_service.annotate_frame, image, identified_products)
    _, buffer = cv2.imencode('.jpg', annotated, [cv2.IMWRITE_JPEG_QUALITY, 80])

    return {
        "detections": identified_products,
        "cart": cart,
        "annotated_frame": base64.b64encode(buffer).decode()
    }



@router.websocket("/detection")
async def detection_websocket(websocket: WebSocket):
    await websocket.accept()
    logger.info("WebSocket client connected for detection")

    # Frame dropping: only process the latest frame
    latest_frame = None
    processing = False
    frame_lock = asyncio.Lock()

    async def process_latest():
        nonlocal latest_frame, processing
        while True:
            frame_to_process = None
            async with frame_lock:
                if latest_frame is not None and not processing:
                    frame_to_process = latest_frame
                    latest_frame = None
                    processing = True

            if frame_to_process is None:
                await asyncio.sleep(0.05)
                continue

            try:
                result = await process_frame(frame_to_process)
                await websocket.send_json(result)
            except Exception as e:
                logger.error(f"Error processing frame: {e}")
                try:
                    await websocket.send_json({"error": str(e)})
                except Exception:
                    return
            finally:
                async with frame_lock:
                    processing = False

    # Start the frame processor task
    processor_task = asyncio.create_task(process_latest())

    try:
        while True:
            # Receive frame from frontend
            data = await websocket.receive_text()
            message = json.loads(data)

            if message.get("type") == "frame":
                # Decode base64 image
                frame_data = message["data"]
                # Remove data URL prefix if present
                if "," in frame_data:
                    frame_data = frame_data.split(",")[1]

                img_bytes = base64.b64decode(frame_data)
                nparr = np.frombuffer(img_bytes, np.uint8)
                image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

                if image is None:
                    await websocket.send_json({"error": "Could not decode image"})
                    continue

                # Store as latest frame (drops old unprocessed frames)
                async with frame_lock:
                    latest_frame = image

            elif message.get("type") == "ping":
                await websocket.send_json({"type": "pong"})

    except WebSocketDisconnect:
        logger.info("WebSocket client disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        processor_task.cancel()
        try:
            await websocket.close()
        except Exception:
            pass
