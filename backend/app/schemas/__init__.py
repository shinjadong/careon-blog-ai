"""
Pydantic schemas package
"""
from app.schemas.device import (
    DeviceInfo,
    DeviceProfileCreate,
    DeviceProfileUpdate,
    DeviceProfileResponse,
    DeviceListResponse,
    DeviceConnectionStatus,
)
from app.schemas.coordinate import (
    CoordinatePoint,
    CoordinateCreate,
    CoordinateUpdate,
    CoordinateResponse,
    CoordinateListResponse,
    CoordinateBatchCreate,
    CalibrationSession,
    CalibrationResult,
    CalibrationGuide,
)

__all__ = [
    # Device schemas
    "DeviceInfo",
    "DeviceProfileCreate",
    "DeviceProfileUpdate",
    "DeviceProfileResponse",
    "DeviceListResponse",
    "DeviceConnectionStatus",
    # Coordinate schemas
    "CoordinatePoint",
    "CoordinateCreate",
    "CoordinateUpdate",
    "CoordinateResponse",
    "CoordinateListResponse",
    "CoordinateBatchCreate",
    "CalibrationSession",
    "CalibrationResult",
    "CalibrationGuide",
]
