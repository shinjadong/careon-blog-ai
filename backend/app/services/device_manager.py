"""
Device Manager Service - Production-grade device profile management

Handles device discovery, profile creation, and coordinate management
"""
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from loguru import logger

from app.models.device import DeviceProfile
from app.models.coordinate import CoordinateConfig, UIElementType, CalibrationMethod
from app.schemas.device import DeviceProfileCreate, DeviceProfileUpdate
from app.schemas.coordinate import CoordinateCreate, CoordinateUpdate
from app.services.adb_controller import ADBController, list_connected_devices


class DeviceManager:
    """
    Production-grade device profile manager

    Responsibilities:
    - Device discovery and profile creation
    - Profile CRUD operations
    - Coordinate configuration management
    - Calibration tracking
    """

    def __init__(self, db: Session):
        """
        Initialize device manager

        Args:
            db: SQLAlchemy database session
        """
        self.db = db

    def scan_devices(self) -> List[dict]:
        """
        Scan for connected ADB devices

        Returns:
            List of device information dictionaries
        """
        try:
            devices = list_connected_devices()
            logger.info(f"Found {len(devices)} connected devices")
            return devices

        except Exception as e:
            logger.error(f"Device scan failed: {e}")
            return []

    def get_or_create_profile(self, device_info: dict) -> DeviceProfile:
        """
        Get existing profile or create new one for device

        Args:
            device_info: Device information dictionary

        Returns:
            DeviceProfile instance
        """
        try:
            # Generate profile ID
            profile_id = DeviceProfile.generate_profile_id(
                model=device_info["model"],
                width=device_info["width"],
                height=device_info["height"],
            )

            # Check if profile exists
            profile = (
                self.db.query(DeviceProfile)
                .filter(DeviceProfile.profile_id == profile_id)
                .first()
            )

            if profile:
                # Profile exists - add device ID if new
                if device_info["device_id"] not in profile.device_ids:
                    device_ids = profile.device_ids.copy()
                    device_ids.append(device_info["device_id"])
                    profile.device_ids = device_ids
                    profile.last_used_at = datetime.utcnow()
                    self.db.commit()
                    logger.info(
                        f"Added device {device_info['device_id']} to existing profile {profile_id}"
                    )
            else:
                # Create new profile
                profile = DeviceProfile(
                    profile_id=profile_id,
                    model=device_info["model"],
                    manufacturer=device_info["manufacturer"],
                    android_version=device_info["android_version"],
                    width=device_info["width"],
                    height=device_info["height"],
                    dpi=device_info["dpi"],
                    device_ids=[device_info["device_id"]],
                    calibrated=False,
                    calibration_confidence=0.0,
                )
                self.db.add(profile)
                self.db.commit()
                self.db.refresh(profile)

                # Initialize default coordinates
                self._initialize_default_coordinates(profile)

                logger.info(f"Created new profile: {profile_id}")

            return profile

        except Exception as e:
            logger.error(f"Failed to get/create profile: {e}")
            self.db.rollback()
            raise

    def _initialize_default_coordinates(self, profile: DeviceProfile):
        """
        Initialize default coordinates based on resolution

        Args:
            profile: DeviceProfile instance
        """
        try:
            w = profile.width
            h = profile.height

            # Define default coordinates based on common UI positions
            default_coords = [
                {
                    "element_type": UIElementType.WRITE_BUTTON,
                    "element_name": "+ 아이콘 (메인 화면)",
                    "x": int(w * 0.85),
                    "y": int(h * 0.93),
                    "description": "메인 화면 우하단 + 아이콘",
                },
                {
                    "element_type": UIElementType.HOME_BUTTON,
                    "element_name": "블로그 글쓰기 버튼",
                    "x": int(w * 0.50),
                    "y": int(h * 0.60),
                    "description": "+ 아이콘 클릭 후 나타나는 블로그 글쓰기 메뉴",
                },
                {
                    "element_type": UIElementType.TITLE_FIELD,
                    "element_name": "제목 입력 필드",
                    "x": int(w * 0.50),
                    "y": int(h * 0.15),
                    "description": "에디터 상단 제목 입력 영역",
                },
                {
                    "element_type": UIElementType.CONTENT_FIELD,
                    "element_name": "본문 입력 필드",
                    "x": int(w * 0.50),
                    "y": int(h * 0.40),
                    "description": "에디터 본문 입력 영역",
                },
                {
                    "element_type": UIElementType.IMAGE_BUTTON,
                    "element_name": "이미지 추가 버튼",
                    "x": int(w * 0.15),
                    "y": int(h * 0.93),
                    "description": "에디터 하단 이미지 추가 버튼",
                },
                {
                    "element_type": UIElementType.PUBLISH_BUTTON,
                    "element_name": "발행 버튼",
                    "x": int(w * 0.90),
                    "y": int(h * 0.08),
                    "description": "에디터 상단 우측 발행 버튼",
                },
                {
                    "element_type": UIElementType.TEXT_SIZE_BUTTON,
                    "element_name": "텍스트 크기 버튼",
                    "x": int(w * 0.70),
                    "y": int(h * 0.93),
                    "description": "에디터 하단 텍스트 크기 변경 버튼 (가 아이콘)",
                },
                {
                    "element_type": UIElementType.BOLD_BUTTON,
                    "element_name": "최소 텍스트 크기",
                    "x": int(w * 0.20),
                    "y": int(h * 0.70),
                    "description": "텍스트 크기 팝업에서 가장 작은 크기",
                },
                {
                    "element_type": UIElementType.LINK_BUTTON,
                    "element_name": "링크 추가 버튼",
                    "x": int(w * 0.65),
                    "y": int(h * 0.85),
                    "description": "이미지 선택 후 링크 추가 버튼",
                },
                {
                    "element_type": UIElementType.CONFIRM_BUTTON,
                    "element_name": "확인 버튼",
                    "x": int(w * 0.65),
                    "y": int(h * 0.60),
                    "description": "일반 확인 버튼",
                },
                {
                    "element_type": UIElementType.SHARE_BUTTON,
                    "element_name": "공유 버튼",
                    "x": int(w * 0.90),
                    "y": int(h * 0.08),
                    "description": "발행 후 공유 버튼",
                },
                {
                    "element_type": UIElementType.COPY_LINK_BUTTON,
                    "element_name": "링크 복사 버튼",
                    "x": int(w * 0.50),
                    "y": int(h * 0.50),
                    "description": "URL 링크 복사 버튼",
                },
            ]

            for coord_data in default_coords:
                coord = CoordinateConfig(
                    profile_id=profile.profile_id,
                    element_type=coord_data["element_type"],
                    element_name=coord_data["element_name"],
                    element_description=coord_data.get("description", ""),
                    x=coord_data["x"],
                    y=coord_data["y"],
                    confidence=0.5,  # Low confidence for defaults
                    validated=False,
                    calibration_method=CalibrationMethod.DEFAULT,
                )
                self.db.add(coord)

            self.db.commit()
            logger.info(
                f"Initialized {len(default_coords)} default coordinates for {profile.profile_id}"
            )

        except Exception as e:
            logger.error(f"Failed to initialize default coordinates: {e}")
            self.db.rollback()

    def get_profile(self, profile_id: str) -> Optional[DeviceProfile]:
        """
        Get device profile by ID

        Args:
            profile_id: Profile ID

        Returns:
            DeviceProfile or None
        """
        return (
            self.db.query(DeviceProfile)
            .filter(DeviceProfile.profile_id == profile_id)
            .first()
        )

    def list_profiles(
        self, skip: int = 0, limit: int = 100
    ) -> tuple[List[DeviceProfile], int]:
        """
        List all device profiles with pagination

        Args:
            skip: Number of records to skip
            limit: Maximum records to return

        Returns:
            Tuple of (profiles list, total count)
        """
        total = self.db.query(DeviceProfile).count()
        profiles = self.db.query(DeviceProfile).offset(skip).limit(limit).all()
        return profiles, total

    def update_profile(
        self, profile_id: str, update_data: DeviceProfileUpdate
    ) -> Optional[DeviceProfile]:
        """
        Update device profile

        Args:
            profile_id: Profile ID
            update_data: Update data

        Returns:
            Updated DeviceProfile or None
        """
        try:
            profile = self.get_profile(profile_id)
            if not profile:
                return None

            # Update fields
            if update_data.notes is not None:
                profile.notes = update_data.notes
            if update_data.calibrated is not None:
                profile.calibrated = update_data.calibrated
            if update_data.calibration_confidence is not None:
                profile.calibration_confidence = update_data.calibration_confidence

            profile.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(profile)

            logger.info(f"Updated profile: {profile_id}")
            return profile

        except Exception as e:
            logger.error(f"Failed to update profile: {e}")
            self.db.rollback()
            return None

    def delete_profile(self, profile_id: str) -> bool:
        """
        Delete device profile and all associated coordinates

        Args:
            profile_id: Profile ID

        Returns:
            True if deleted successfully
        """
        try:
            profile = self.get_profile(profile_id)
            if not profile:
                return False

            self.db.delete(profile)
            self.db.commit()

            logger.info(f"Deleted profile: {profile_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete profile: {e}")
            self.db.rollback()
            return False

    # Coordinate Management

    def get_coordinates(
        self, profile_id: str, element_type: Optional[UIElementType] = None
    ) -> List[CoordinateConfig]:
        """
        Get coordinate configurations for profile

        Args:
            profile_id: Profile ID
            element_type: Optional filter by element type

        Returns:
            List of CoordinateConfig instances
        """
        query = self.db.query(CoordinateConfig).filter(
            CoordinateConfig.profile_id == profile_id
        )

        if element_type:
            query = query.filter(CoordinateConfig.element_type == element_type)

        return query.all()

    def get_coordinate(self, coord_id: int) -> Optional[CoordinateConfig]:
        """Get single coordinate by ID"""
        return (
            self.db.query(CoordinateConfig)
            .filter(CoordinateConfig.id == coord_id)
            .first()
        )

    def create_coordinate(
        self, coord_data: CoordinateCreate
    ) -> Optional[CoordinateConfig]:
        """
        Create new coordinate configuration

        Args:
            coord_data: Coordinate data

        Returns:
            Created CoordinateConfig or None
        """
        try:
            coord = CoordinateConfig(
                profile_id=coord_data.profile_id,
                element_type=UIElementType(coord_data.element_type),
                element_name=coord_data.element_name,
                element_description=coord_data.element_description,
                x=coord_data.x,
                y=coord_data.y,
                confidence=coord_data.confidence,
                validated=coord_data.validated,
                calibration_method=CalibrationMethod(coord_data.calibration_method),
                calibrated_by=coord_data.calibrated_by,
                calibrated_at=datetime.utcnow(),
                touch_radius=coord_data.touch_radius,
                notes=coord_data.notes,
            )
            self.db.add(coord)
            self.db.commit()
            self.db.refresh(coord)

            logger.info(f"Created coordinate: {coord.element_name} at ({coord.x}, {coord.y})")
            return coord

        except Exception as e:
            logger.error(f"Failed to create coordinate: {e}")
            self.db.rollback()
            return None

    def update_coordinate(
        self, coord_id: int, update_data: CoordinateUpdate
    ) -> Optional[CoordinateConfig]:
        """
        Update coordinate configuration

        Args:
            coord_id: Coordinate ID
            update_data: Update data

        Returns:
            Updated CoordinateConfig or None
        """
        try:
            coord = self.get_coordinate(coord_id)
            if not coord:
                return None

            # Update fields
            if update_data.x is not None:
                coord.x = update_data.x
            if update_data.y is not None:
                coord.y = update_data.y
            if update_data.confidence is not None:
                coord.confidence = update_data.confidence
            if update_data.validated is not None:
                coord.validated = update_data.validated
            if update_data.calibration_method is not None:
                coord.calibration_method = CalibrationMethod(
                    update_data.calibration_method
                )
            if update_data.calibrated_by is not None:
                coord.calibrated_by = update_data.calibrated_by
            if update_data.touch_radius is not None:
                coord.touch_radius = update_data.touch_radius
            if update_data.notes is not None:
                coord.notes = update_data.notes

            coord.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(coord)

            logger.info(f"Updated coordinate: {coord_id}")
            return coord

        except Exception as e:
            logger.error(f"Failed to update coordinate: {e}")
            self.db.rollback()
            return None

    def delete_coordinate(self, coord_id: int) -> bool:
        """
        Delete coordinate configuration

        Args:
            coord_id: Coordinate ID

        Returns:
            True if deleted successfully
        """
        try:
            coord = self.get_coordinate(coord_id)
            if not coord:
                return False

            self.db.delete(coord)
            self.db.commit()

            logger.info(f"Deleted coordinate: {coord_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete coordinate: {e}")
            self.db.rollback()
            return False
