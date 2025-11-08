"""
Device Profile Database Model
"""
from sqlalchemy import Column, String, Integer, Boolean, DateTime, JSON, Float
from sqlalchemy.orm import relationship
from datetime import datetime
import hashlib

from app.core.database import Base


class DeviceProfile(Base):
    """
    Device profile model for storing device metadata and configuration

    A profile represents a unique device configuration (model + resolution).
    Multiple physical devices with same specs can share one profile.
    """

    __tablename__ = "device_profiles"

    # Primary Key
    profile_id = Column(String(64), primary_key=True, index=True)

    # Device Information
    model = Column(String(100), nullable=False)
    manufacturer = Column(String(100), nullable=False)
    android_version = Column(String(20), nullable=False)

    # Display Specifications
    width = Column(Integer, nullable=False)
    height = Column(Integer, nullable=False)
    dpi = Column(Integer, nullable=False)

    # Device IDs (multiple devices can share same profile)
    device_ids = Column(JSON, default=list)  # List of ADB serial numbers

    # Calibration Status
    calibrated = Column(Boolean, default=False)
    calibration_confidence = Column(Float, default=0.0)

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)

    # Notes
    notes = Column(String(500), nullable=True)

    # Relationships
    coordinates = relationship(
        "CoordinateConfig",
        back_populates="profile",
        cascade="all, delete-orphan",
    )

    @staticmethod
    def generate_profile_id(model: str, width: int, height: int) -> str:
        """
        Generate unique profile ID based on device specs

        Format: {model}_{resolution}_{hash}
        Example: Samsung_Galaxy_S21_1080x2400_a3f8b2c1
        """
        base = f"{model}_{width}x{height}"
        hash_suffix = hashlib.md5(base.encode()).hexdigest()[:8]
        return f"{base.replace(' ', '_')}_{hash_suffix}"

    def add_device_id(self, device_id: str):
        """Add a new device ID to this profile"""
        if device_id not in self.device_ids:
            self.device_ids.append(device_id)

    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            "profile_id": self.profile_id,
            "model": self.model,
            "manufacturer": self.manufacturer,
            "android_version": self.android_version,
            "resolution": {"width": self.width, "height": self.height},
            "dpi": self.dpi,
            "device_ids": self.device_ids,
            "calibrated": self.calibrated,
            "calibration_confidence": self.calibration_confidence,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_used_at": (
                self.last_used_at.isoformat() if self.last_used_at else None
            ),
            "notes": self.notes,
        }
