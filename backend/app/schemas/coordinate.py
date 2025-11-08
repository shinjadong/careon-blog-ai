"""
Coordinate Configuration Pydantic Schemas for API validation
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class CoordinatePoint(BaseModel):
    """Simple coordinate point"""

    x: int = Field(..., ge=0, description="X coordinate in pixels")
    y: int = Field(..., ge=0, description="Y coordinate in pixels")


class CoordinateCreate(BaseModel):
    """Schema for creating new coordinate configuration"""

    profile_id: str = Field(..., description="Device profile ID")
    element_type: str = Field(..., description="UI element type")
    element_name: str = Field(..., min_length=1, max_length=100)
    element_description: Optional[str] = Field(None, max_length=500)
    x: int = Field(..., ge=0)
    y: int = Field(..., ge=0)
    confidence: float = Field(0.5, ge=0.0, le=1.0)
    validated: bool = Field(False)
    calibration_method: str = Field("user_click")
    calibrated_by: Optional[str] = Field(None, max_length=100)
    touch_radius: int = Field(20, ge=1, le=200)
    notes: Optional[str] = Field(None, max_length=500)

    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v):
        if not (0.0 <= v <= 1.0):
            raise ValueError("Confidence must be between 0.0 and 1.0")
        return v


class CoordinateUpdate(BaseModel):
    """Schema for updating coordinate configuration"""

    x: Optional[int] = Field(None, ge=0)
    y: Optional[int] = Field(None, ge=0)
    confidence: Optional[float] = Field(None, ge=0.0, le=1.0)
    validated: Optional[bool] = None
    calibration_method: Optional[str] = None
    calibrated_by: Optional[str] = None
    touch_radius: Optional[int] = Field(None, ge=1, le=200)
    notes: Optional[str] = Field(None, max_length=500)


class CoordinateResponse(BaseModel):
    """Schema for coordinate configuration API response"""

    id: int
    profile_id: str
    element_type: str
    element_name: str
    element_description: Optional[str]
    coordinates: dict[str, int]  # {"x": 100, "y": 200}
    confidence: float
    validated: bool
    calibration_method: str
    calibrated_by: Optional[str]
    calibrated_at: Optional[str]
    touch_radius: int
    usage_stats: dict[str, float | int]  # usage_count, success_rate, etc.
    created_at: Optional[str]
    updated_at: Optional[str]
    last_used_at: Optional[str]
    notes: Optional[str]

    class Config:
        from_attributes = True


class CoordinateListResponse(BaseModel):
    """Schema for list of coordinates"""

    total: int
    coordinates: list[CoordinateResponse]


class CoordinateBatchCreate(BaseModel):
    """Schema for batch creating coordinates"""

    profile_id: str
    coordinates: list[dict]  # List of coordinate configs


class CalibrationSession(BaseModel):
    """Schema for calibration session tracking"""

    session_id: str
    profile_id: str
    current_step: int
    total_steps: int
    element_type: str
    element_name: str
    instructions: str
    screenshot_url: Optional[str] = None
    completed: bool = False


class CalibrationResult(BaseModel):
    """Schema for calibration result"""

    session_id: str
    element_type: str
    x: int = Field(..., ge=0)
    y: int = Field(..., ge=0)
    calibrated_by: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class CalibrationGuide(BaseModel):
    """Schema for calibration step guide"""

    step_number: int
    element_type: str
    element_name: str
    instructions: str
    help_text: Optional[str] = None
    example_image: Optional[str] = None
