"""
UI Coordinate Configuration Database Model
"""
from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from app.core.database import Base


class UIElementType(str, enum.Enum):
    """
    UI element types for Naver Blog app

    Updated naming for clarity and consistency (2025-11-08)
    """

    # Main Navigation (Step 1-2)
    MAIN_PLUS_BUTTON = "main_plus_button"  # + 아이콘 (메인 화면)
    WRITE_MENU_BLOG = "write_menu_blog"    # 블로그 글쓰기 메뉴 버튼

    # Editor Fields (Step 3-4)
    TITLE_FIELD = "title_field"            # 제목 입력 필드
    CONTENT_FIELD = "content_field"        # 본문 입력 필드

    # Editor Toolbar (Step 5-8)
    IMAGE_BUTTON = "image_button"          # 이미지 추가 버튼
    TEXT_SIZE_BUTTON = "text_size_button"  # 텍스트 크기 버튼
    TEXT_SIZE_SMALLEST = "text_size_smallest"  # 최소 크기 선택
    LINK_BUTTON = "link_button"            # 링크 추가 버튼

    # Publishing (Step 9-10)
    PUBLISH_BUTTON = "publish_button"      # 발행 버튼
    CONFIRM_BUTTON = "confirm_button"      # 확인 버튼

    # Sharing (Step 11-12)
    SHARE_BUTTON = "share_button"          # 공유 버튼
    COPY_URL_BUTTON = "copy_url_button"    # 링크 복사 버튼

    # Optional/Future
    MENU_BUTTON = "menu_button"
    PUBLISH_SETTINGS_BUTTON = "publish_settings_button"
    CANCEL_BUTTON = "cancel_button"

    # Gallery (for image selection)
    GALLERY_FIRST_IMAGE = "gallery_first_image"
    GALLERY_SELECT_BUTTON = "gallery_select_button"

    # Deprecated (no longer used)
    TEXT_COLOR_BUTTON = "text_color_button"  # @deprecated: Use TEXT_SIZE instead
    WHITE_COLOR = "white_color"              # @deprecated: Use TEXT_SIZE_SMALLEST
    BLACK_COLOR = "black_color"              # @deprecated
    COLOR_PICKER = "color_picker"            # @deprecated
    BOLD_BUTTON = "bold_button"              # @deprecated: Use TEXT_SIZE_SMALLEST

    # Aliases (backward compatibility)
    WRITE_BUTTON = "main_plus_button"       # Alias for MAIN_PLUS_BUTTON
    HOME_BUTTON = "write_menu_blog"         # Alias for WRITE_MENU_BLOG


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
