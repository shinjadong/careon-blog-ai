"""
UI Coordinate Configuration Database Model
"""
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class UIElementType(str, enum.Enum):
    """UI element types for Naver Blog app"""

    # Main Navigation
    WRITE_BUTTON = "write_button"
    HOME_BUTTON = "home_button"
    MENU_BUTTON = "menu_button"

    # Editor Elements
    TITLE_FIELD = "title_field"
    CONTENT_FIELD = "content_field"
    IMAGE_BUTTON = "image_button"
    LINK_BUTTON = "link_button"
    TEXT_COLOR_BUTTON = "text_color_button"
    TEXT_SIZE_BUTTON = "text_size_button"
    BOLD_BUTTON = "bold_button"

    # Color Palette
    WHITE_COLOR = "white_color"
    BLACK_COLOR = "black_color"
    COLOR_PICKER = "color_picker"

    # Publishing
    PUBLISH_BUTTON = "publish_button"
    PUBLISH_SETTINGS_BUTTON = "publish_settings_button"
    CONFIRM_BUTTON = "confirm_button"
    CANCEL_BUTTON = "cancel_button"

    # Share & URL
    SHARE_BUTTON = "share_button"
    COPY_LINK_BUTTON = "copy_link_button"

    # Gallery
    GALLERY_FIRST_IMAGE = "gallery_first_image"
    GALLERY_SELECT_BUTTON = "gallery_select_button"

    # Custom (사용자 정의)
    CUSTOM = "custom"


class CalibrationMethod(str, enum.Enum):
    """Method used for coordinate calibration"""

    USER_CLICK = "user_click"  # 사용자가 직접 클릭
    MANUAL_INPUT = "manual_input"  # 수동 입력
    AI_VISION = "ai_vision"  # AI Vision 분석
    DEFAULT = "default"  # 기본값 (해상도 비율 기반)


class CoordinateConfig(Base):
    """
    UI coordinate configuration for specific device profile

    Stores exact pixel coordinates for all UI elements needed for automation
    """

    __tablename__ = "coordinate_configs"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Foreign Key to DeviceProfile
    profile_id = Column(String(64), ForeignKey("device_profiles.profile_id"))

    # UI Element Identification
    element_type = Column(Enum(UIElementType), nullable=False, index=True)
    element_name = Column(String(100), nullable=False)  # Human-readable name
    element_description = Column(String(500), nullable=True)  # 설명

    # Coordinate Data
    x = Column(Integer, nullable=False)
    y = Column(Integer, nullable=False)

    # Confidence & Validation
    confidence = Column(Float, default=0.5)  # 0.0 ~ 1.0
    validated = Column(Boolean, default=False)  # 실제 테스트 완료 여부

    # Calibration Info
    calibration_method = Column(
        Enum(CalibrationMethod), default=CalibrationMethod.DEFAULT
    )
    calibrated_by = Column(String(100), nullable=True)  # 캘리브레이션 수행자
    calibrated_at = Column(DateTime, nullable=True)

    # Optional: 클릭 가능 영역 (터치 타겟이 넓을 경우)
    touch_radius = Column(Integer, default=20)  # pixels

    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_used_at = Column(DateTime, nullable=True)

    # Usage Statistics
    usage_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    fail_count = Column(Integer, default=0)

    # Notes
    notes = Column(String(500), nullable=True)

    # Relationship
    profile = relationship("DeviceProfile", back_populates="coordinates")

    @property
    def success_rate(self) -> float:
        """Calculate success rate"""
        if self.usage_count == 0:
            return 0.0
        return self.success_count / self.usage_count

    def increment_usage(self, success: bool = True):
        """Increment usage statistics"""
        self.usage_count += 1
        if success:
            self.success_count += 1
        else:
            self.fail_count += 1
        self.last_used_at = datetime.utcnow()

    def to_dict(self) -> dict:
        """Convert to dictionary for API responses"""
        return {
            "id": self.id,
            "profile_id": self.profile_id,
            "element_type": self.element_type.value,
            "element_name": self.element_name,
            "element_description": self.element_description,
            "coordinates": {"x": self.x, "y": self.y},
            "confidence": self.confidence,
            "validated": self.validated,
            "calibration_method": self.calibration_method.value,
            "calibrated_by": self.calibrated_by,
            "calibrated_at": (
                self.calibrated_at.isoformat() if self.calibrated_at else None
            ),
            "touch_radius": self.touch_radius,
            "usage_stats": {
                "usage_count": self.usage_count,
                "success_count": self.success_count,
                "fail_count": self.fail_count,
                "success_rate": self.success_rate,
            },
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_used_at": (
                self.last_used_at.isoformat() if self.last_used_at else None
            ),
            "notes": self.notes,
        }
