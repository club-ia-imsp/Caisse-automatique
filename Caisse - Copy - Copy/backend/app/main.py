import logging
import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import settings
from app.database import async_session
from app.utils.security import hash_password
from app.models.user import AdminUser
from app.api import auth, products, detection, invoices

from sqlalchemy import select, text

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def wait_for_db(retries: int = 10, delay: float = 3.0):
    """Wait for the database to be ready before proceeding."""
    for attempt in range(1, retries + 1):
        try:
            async with async_session() as session:
                await session.execute(text("SELECT 1"))
            logger.info("✅ Database connection established")
            return
        except Exception as e:
            logger.warning(f"⏳ DB not ready (attempt {attempt}/{retries}): {e}")
            if attempt < retries:
                await asyncio.sleep(delay)
    raise RuntimeError("❌ Could not connect to database after multiple attempts")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🚀 automaticCHECK Backend Starting...")

    # Wait for DB to be ready
    await wait_for_db()

    # Create default admin if not exists
    async with async_session() as session:
        result = await session.execute(select(AdminUser).limit(1))
        admin = result.scalar_one_or_none()
        if admin is None:
            default_admin = AdminUser(
                username=settings.DEFAULT_ADMIN_USERNAME,
                email="admin@automaticcheck.com",
                hashed_password=hash_password(settings.DEFAULT_ADMIN_PASSWORD),
                is_active=True
            )
            session.add(default_admin)
            await session.commit()
            logger.info(f"✅ Default admin created: {settings.DEFAULT_ADMIN_USERNAME}")
        else:
            logger.info("✅ Admin user already exists")

    # Initialize AI service
    from app.services.ai_service import ai_service
    ai_service.initialize()
    logger.info("✅ AI Service initialized (YOLO + ResNet18)")

    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

    logger.info("✅ automaticCHECK Backend Ready!")
    yield
    # Shutdown
    logger.info("🛑 automaticCHECK Backend Shutting Down...")


app = FastAPI(
    title="automaticCHECK API",
    description="Caisse Automatique Intelligente - API Backend",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files for uploads
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# API Routes
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/api/products", tags=["Products"])
app.include_router(invoices.router, prefix="/api/invoices", tags=["Invoices"])
app.include_router(detection.router, prefix="/ws", tags=["Detection"])


@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "automaticCHECK API", "version": "1.0.0"}
