# ─────────────────────────────────────────────
#  automaticCHECK — Backend FastAPI
#  Build context : Caisse/   (racine du dossier Caisse)
# ─────────────────────────────────────────────
FROM python:3.11-slim

WORKDIR /app

# Dépendances système requises par opencv-headless et torch
RUN apt-get update && apt-get install -y --no-install-recommends \
        libglib2.0-0 \
        libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Installation des dépendances Python
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# Modèle YOLO (placé à la racine de Caisse/)
COPY best_caisse.pt /app/best_caisse.pt

# Code applicatif
COPY backend/app /app/app

# Dossiers d'uploads (remplacés par un volume Docker en prod)
RUN mkdir -p /app/uploads/products /app/uploads/invoices

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
