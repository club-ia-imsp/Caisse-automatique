@echo off
cd /d "C:\Users\SARA\Desktop\Caisse - Copy\backend"

set PYTHONPATH=C:\Users\SARA\Desktop\Caisse - Copy\backend
set DATABASE_URL=postgresql+asyncpg://foodlink:foodlink_secure_2024@localhost:5432/foodlink_db
set UPLOAD_DIR=C:/Users/SARA/Desktop/Caisse - Copy/backend/uploads
set YOLO_MODEL=C:\Users\SARA\Desktop\Caisse - Copy\best_caisse.pt
set SECRET_KEY=foodlink-super-secret-key-change-in-production-2024
set ALGORITHM=HS256
set ACCESS_TOKEN_EXPIRE_MINUTES=480
set DEFAULT_ADMIN_USERNAME=admin
set DEFAULT_ADMIN_PASSWORD=admin123
set EMBEDDING_DIM=512
set SIMILARITY_THRESHOLD=0.30

"C:\Users\SARA\Desktop\Caisse - Copy\.venv\Scripts\python.exe" -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
pause
