import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://foodlink:foodlink_secure_2024@db:5432/foodlink_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "foodlink-super-secret-key-change-in-production-2024")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "480"))

    DEFAULT_ADMIN_USERNAME: str = os.getenv("DEFAULT_ADMIN_USERNAME", "admin")
    DEFAULT_ADMIN_PASSWORD: str = os.getenv("DEFAULT_ADMIN_PASSWORD", "admin123")

    YOLO_MODEL: str = os.getenv("YOLO_MODEL", "yolo11n.pt")
    EMBEDDING_DIM: int = int(os.getenv("EMBEDDING_DIM", "512"))
    SIMILARITY_THRESHOLD: float = float(os.getenv("SIMILARITY_THRESHOLD", "0.30"))

    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "/app/uploads")
    TAX_RATE: float = 0.18  # TVA 18%


settings = Settings()
