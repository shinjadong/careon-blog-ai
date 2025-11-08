"""
Device Profile Pydantic Schemas for API validation
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class DeviceInfo(BaseModel):
    """Raw device information from ADB"""

    device_id: str = Field(..., description="ADB serial number")
    model: str = Field(..., description="Device model name")
    manufacturer: str = Field(..., description="Device manufacturer")
    android_version: str = Field(..., description="Android OS version")
    width: int = Field(..., gt=0, description="Screen width in pixels")
    height: int = Field(..., gt=0, description="Screen height in pixels")
    dpi: int = Field(..., gt=0, description="Screen density (DPI)")


class DeviceProfileCreate(BaseModel):
    """Schema for creating new device profile"""

    model: str = Field(..., min_length=1, max_length=100)
    manufacturer: str = Field(..., min_length=1, max_length=100)
    android_version: str = Field(..., min_length=1, max_length=20)
    width: int = Field(..., gt=0, le=10000)
    height: int = Field(..., gt=0, le=10000)
    dpi: int = Field(..., gt=0, le=1000)
    device_ids: list[str] = Field(default_factory=list)
    notes: Optional[str] = Field(None, max_length=500)


class DeviceProfileUpdate(BaseModel):
    """Schema for updating device profile"""

    notes: Optional[str] = Field(None, max_length=500)
    calibrated: Optional[bool] = None
    calibration_confidence: Optional[float] = Field(None, ge=0.0, le=1.0)

    @field_validator("calibration_confidence")
    @classmethod
    def validate_confidence(cls, v):
        if v is not None and not (0.0 <= v <= 1.0):
            raise ValueError("Confidence must be between 0.0 and 1.0")
        return v


class DeviceProfileResponse(BaseModel):
    """Schema for device profile API response"""

    profile_id: str
    model: str
    manufacturer: str
    android_version: str
    resolution: dict[str, int]  # {"width": 1080, "height": 2400}
    dpi: int
    device_ids: list[str]
    calibrated: bool
    calibration_confidence: float
    created_at: Optional[str]
    updated_at: Optional[str]
    last_used_at: Optional[str]
    notes: Optional[str]
    coordinate_count: Optional[int] = 0  # Number of configured coordinates

    class Config:
        from_attributes = True


class DeviceListResponse(BaseModel):
    """Schema for list of devices"""

    total: int
    devices: list[DeviceProfileResponse]


class DeviceConnectionStatus(BaseModel):
    """Schema for device connection status"""

    device_id: str
    connected: bool
    model: Optional[str] = None
    profile_id: Optional[str] = None
    last_seen: Optional[datetime] = None
