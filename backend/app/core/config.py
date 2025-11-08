"""
Core configuration for CareOn Blog Automation System
"""
from pydantic_settings import BaseSettings
from pathlib import Path
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "CareOn Blog Automation"
    VERSION: str = "1.0.0"
    DEBUG: bool = True

    # CORS Settings
    BACKEND_CORS_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ]

    # Database Settings
    DATABASE_URL: str = "sqlite:///./data/database.db"

    # File Storage
    DATA_DIR: Path = Path("./data")
    PROFILES_DIR: Path = DATA_DIR / "profiles"
    SCREENSHOTS_DIR: Path = DATA_DIR / "screenshots"

    # ADB Settings
    ADB_SERVER_HOST: str = "127.0.0.1"
    ADB_SERVER_PORT: int = 5037
    ADB_TIMEOUT: int = 30  # seconds

    # Device Settings
    DEFAULT_SCREENSHOT_QUALITY: int = 80
    SCREENSHOT_TIMEOUT: int = 10  # seconds
    TAP_DELAY_MS: int = 300
    SWIPE_DURATION_MS: int = 300

    # Calibration Settings
    MIN_CONFIDENCE_SCORE: float = 0.8
    CALIBRATION_GUIDE_ENABLED: bool = True

    # WebSocket Settings
    WS_HEARTBEAT_INTERVAL: int = 30
    WS_MAX_CONNECTIONS: int = 10

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = "./logs/app.log"

    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Initialize directories
def init_directories():
    """Create necessary directories if they don't exist"""
    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
    settings.PROFILES_DIR.mkdir(parents=True, exist_ok=True)
    settings.SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

    # Create logs directory
    if settings.LOG_FILE:
        Path(settings.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)


init_directories()
