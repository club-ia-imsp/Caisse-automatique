"""
AI Service - best_caisse.pt YOLO for direct class detection.
Mirrors the PyQt5 caisseAutomat.py approach:
  detections → class names (e.g. 'banane', 'couteau') → match to DB products by name.
ResNet18 embedding model is lazy-loaded only when needed for product training.
"""

import logging
import numpy as np
import cv2
import torch
import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights
from torchvision import transforms
from ultralytics import YOLO
from PIL import Image

from app.config import settings

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self):
        self.yolo_model = None
        self.embedding_model = None
        self.transform = None
        self._initialized = False

    def initialize(self):
        if self._initialized:
            return
        logger.info("Loading YOLO model...")
        self.yolo_model = YOLO(settings.YOLO_MODEL)
        self._initialized = True
        logger.info(f"AI Service ready (YOLO: {settings.YOLO_MODEL})")

    def _ensure_embedding_model(self):
        """Lazy-load ResNet18 — only called when training product images."""
        if self.embedding_model is not None:
            return
        logger.info("Loading ResNet18 embedding model (for training)...")
        base_model = resnet18(weights=ResNet18_Weights.DEFAULT)
        self.embedding_model = nn.Sequential(*list(base_model.children())[:-1])
        self.embedding_model.eval()
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])
        logger.info("ResNet18 ready")


    def detect_objects(self, image: np.ndarray, conf_threshold: float = 0.25):
        """Run YOLO detection on an image. Returns list of bounding boxes."""
        if self.yolo_model is None:
            self.initialize()

        # Resize large images to speed up inference
        h, w = image.shape[:2]
        max_dim = 640
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            image_resized = cv2.resize(image, (int(w * scale), int(h * scale)))
        else:
            scale = 1.0
            image_resized = image

        results = self.yolo_model(image_resized, conf=conf_threshold, verbose=False)
        detections = []

        for result in results:
            for box in result.boxes:
                x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
                # Scale back to original image coordinates
                if scale != 1.0:
                    x1, y1, x2, y2 = x1 / scale, y1 / scale, x2 / scale, y2 / scale
                conf = float(box.conf[0].cpu().numpy())
                cls = int(box.cls[0].cpu().numpy())
                detections.append({
                    "bbox": [float(x1), float(y1), float(x2), float(y2)],
                    "confidence": conf,
                    "class_id": cls,
                    "class_name": result.names[cls]
                })

        return detections

    def extract_embedding(self, image: np.ndarray) -> np.ndarray:
        """Extract a 512-dim embedding from an image crop using ResNet18."""
        self._ensure_embedding_model()

        # Convert BGR (OpenCV) to RGB PIL Image
        if len(image.shape) == 3 and image.shape[2] == 3:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image_rgb = image

        pil_image = Image.fromarray(image_rgb)
        tensor = self.transform(pil_image).unsqueeze(0)

        with torch.no_grad():
            embedding = self.embedding_model(tensor)
            embedding = embedding.squeeze().numpy()
            # L2 normalize
            norm = np.linalg.norm(embedding)
            if norm > 0:
                embedding = embedding / norm

        return embedding.tolist()

    def crop_detection(self, image: np.ndarray, bbox: list) -> np.ndarray:
        """Crop a detection from the image using bounding box."""
        x1, y1, x2, y2 = [int(c) for c in bbox]
        h, w = image.shape[:2]
        x1, y1 = max(0, x1), max(0, y1)
        x2, y2 = min(w, x2), min(h, y2)
        return image[y1:y2, x1:x2]

    def center_crop(self, image: np.ndarray, ratio: float = 0.8) -> np.ndarray:
        """Fallback: center crop if YOLO doesn't detect anything."""
        h, w = image.shape[:2]
        new_h, new_w = int(h * ratio), int(w * ratio)
        top = (h - new_h) // 2
        left = (w - new_w) // 2
        return image[top:top + new_h, left:left + new_w]

    def process_training_image(self, image: np.ndarray) -> tuple:
        """
        Process a training image: detect object, crop, extract embedding.
        Returns (embedding, crop_image) or uses center crop as fallback.
        """
        self._ensure_embedding_model()
        detections = self.detect_objects(image, conf_threshold=0.3)

        if detections:
            # Use the detection with highest confidence
            best = max(detections, key=lambda d: d["confidence"])
            crop = self.crop_detection(image, best["bbox"])
        else:
            # Fallback to center crop
            crop = self.center_crop(image)

        if crop.size == 0:
            crop = self.center_crop(image)

        embedding = self.extract_embedding(crop)
        return embedding, crop

    def annotate_frame(self, image: np.ndarray, detections: list) -> np.ndarray:
        """Draw bounding boxes and labels on the frame for multiple detected products."""
        annotated = image.copy()
        for det in detections:
            bbox = det["bbox"]
            x1, y1, x2, y2 = [int(c) for c in bbox]
            label = det.get("product_name", "Inconnu")
            conf = det.get("similarity", det.get("confidence", 0))
            price = det.get("price", 0)
            is_identified = det.get("product_id") is not None

            # Green for identified, orange for unknown
            if is_identified:
                color = (22, 136, 28)  # Green in BGR
            else:
                color = (0, 140, 255)  # Orange in BGR

            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)

            if is_identified:
                text = f"{label} ({conf:.0%}) - {price:.0f} FCFA"
            else:
                text = f"? {label} ({conf:.0%})"

            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 2)[0]
            cv2.rectangle(annotated, (x1, y1 - text_size[1] - 10), (x1 + text_size[0] + 4, y1), color, -1)
            cv2.putText(annotated, text, (x1 + 2, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 2)

        return annotated


# Singleton instance
ai_service = AIService()
