"""
CareOn Blog Automation System - Main FastAPI Application
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger
import sys

from app.core.config import settings
from app.core.database import Base, engine, init_db
from app.api.v1 import devices, calibration, automation

# Configure logging
logger.remove()
logger.add(
    sys.stderr,
    level=settings.LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)

if settings.LOG_FILE:
    logger.add(
        settings.LOG_FILE,
        rotation="10 MB",
        retention="7 days",
        level=settings.LOG_LEVEL,
    )

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Production-grade mobile blog automation system with interactive device calibration",
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
try:
    app.mount(
        "/screenshots", StaticFiles(directory=str(settings.SCREENSHOTS_DIR)), name="screenshots"
    )
except RuntimeError:
    logger.warning("Screenshots directory not found, skipping static files mount")


# Include API routers
app.include_router(
    devices.router,
    prefix=f"{settings.API_V1_PREFIX}/devices",
    tags=["Devices"],
)

app.include_router(
    calibration.router,
    prefix=f"{settings.API_V1_PREFIX}/calibration",
    tags=["Calibration"],
)

app.include_router(
    automation.router,
    prefix=f"{settings.API_V1_PREFIX}/automation",
    tags=["Automation"],
)


@app.on_event("startup")
async def startup_event():
    """Initialize application on startup"""
    logger.info(f"🚀 Starting {settings.PROJECT_NAME} v{settings.VERSION}")

    # Initialize database
    init_db()
    logger.info("✅ Database initialized")

    # Log configuration
    logger.info(f"📍 API Prefix: {settings.API_V1_PREFIX}")
    logger.info(f"📁 Data Directory: {settings.DATA_DIR}")
    logger.info(f"🔧 Debug Mode: {settings.DEBUG}")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    logger.info("👋 Shutting down application")


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "status": "running",
        "docs_url": "/docs",
        "api_prefix": settings.API_V1_PREFIX,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": settings.VERSION,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
