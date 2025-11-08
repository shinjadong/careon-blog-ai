"""
Automation Executor - Blog Posting Automation Engine

Manus-style AI Agent: Observe → Plan → Execute → Verify
"""
from typing import Optional, List, Dict
from dataclasses import dataclass
from datetime import datetime
from loguru import logger
import time

from app.services.adb_controller import ADBController
from app.services.device_manager import DeviceManager
from app.core.ui_elements import get_ui_elements_ordered, get_element_by_type
from app.models.coordinate import UIElementType
from sqlalchemy.orm import Session


@dataclass
class PostingResult:
    """Result of automated blog posting"""

    success: bool
    blog_url: Optional[str] = None
    error_message: Optional[str] = None
    steps_completed: int = 0
    total_steps: int = 12
    execution_time: float = 0.0
    failed_step: Optional[str] = None


class BlogPostingAutomator:
    """
    Production-grade blog posting automation

    Executes 12-step sequence to publish a blog post automatically
    using saved UI coordinates from device profile.

    Pattern: Observe → Plan → Execute → Verify (Manus-style)
    """

    def __init__(
        self,
        device_id: str,
        profile_id: str,
        db: Session,
        max_retries: int = 3,
    ):
        """
        Initialize automation executor

        Args:
            device_id: ADB device serial
            profile_id: Device profile ID
            db: Database session
            max_retries: Maximum retry attempts per step
        """
        self.device_id = device_id
        self.profile_id = profile_id
        self.db = db
        self.max_retries = max_retries

        # Initialize controllers
        self.adb = ADBController(device_id)
        self.manager = DeviceManager(db)

        # Load profile and coordinates
        self.profile = self.manager.get_profile(profile_id)
        if not self.profile:
            raise ValueError(f"Profile not found: {profile_id}")

        self.coordinates = self._load_coordinates()

        # Statistics
        self.steps_executed = 0
        self.start_time = None

    def _load_coordinates(self) -> Dict[UIElementType, dict]:
        """Load all coordinates for this profile"""
        coords = self.manager.get_coordinates(self.profile_id)
        coord_map = {}

        for coord in coords:
            coord_map[UIElementType(coord.element_type)] = {
                "id": coord.id,
                "x": coord.x,
                "y": coord.y,
                "confidence": coord.confidence,
            }

        logger.info(f"Loaded {len(coord_map)} coordinates for {self.profile_id}")
        return coord_map

    def _get_coordinate(self, element_type: UIElementType) -> dict:
        """Get coordinate for UI element"""
        if element_type not in self.coordinates:
            raise ValueError(f"Coordinate not found for {element_type}")
        return self.coordinates[element_type]

    def _tap_element(
        self,
        element_type: UIElementType,
        delay_ms: int = 800,
    ) -> bool:
        """
        Tap UI element by type

        Args:
            element_type: UI element to tap
            delay_ms: Delay after tap in milliseconds

        Returns:
            True if tap successful
        """
        try:
            coord = self._get_coordinate(element_type)
            element_def = get_element_by_type(element_type)

            logger.info(f"Tapping {element_def.name} at ({coord['x']}, {coord['y']})")

            self.adb.tap(coord["x"], coord["y"], delay_ms=delay_ms)
            return True

        except Exception as e:
            logger.error(f"Failed to tap {element_type}: {e}")
            return False

    def _input_text_smart(self, text: str, field_type: UIElementType) -> bool:
        """
        Input text using clipboard (supports Korean)

        Args:
            text: Text to input
            field_type: Field to input into

        Returns:
            True if input successful
        """
        try:
            # Tap field first
            if not self._tap_element(field_type, delay_ms=500):
                return False

            # Set clipboard and paste
            self.adb.set_clipboard(text)
            time.sleep(0.3)
            self.adb.paste()
            time.sleep(0.5)

            logger.info(f"Input text: {text[:50]}...")
            return True

        except Exception as e:
            logger.error(f"Failed to input text: {e}")
            return False

    async def execute_posting(
        self,
        title: str,
        content: str,
        images: Optional[List[str]] = None,
    ) -> PostingResult:
        """
        Execute complete blog posting sequence

        Steps:
        1. Tap + button (main screen)
        2. Tap "Blog Write" menu
        3. Input title
        4. Input content
        5. Adjust text size (smallest)
        6. Publish
        7. Confirm
        8. Share
        9. Copy URL

        Args:
            title: Blog post title
            content: Blog post content
            images: Optional list of image paths

        Returns:
            PostingResult with success status and blog URL
        """
        self.start_time = time.time()
        result = PostingResult(success=False, total_steps=9)  # 9 core steps

        try:
            # Ensure ADB connection
            if not self.adb.connect():
                result.error_message = "Failed to connect to device"
                return result

            logger.info(f"🚀 Starting automated posting for {self.profile_id}")

            # Step 1: Tap + button (main screen)
            logger.info("Step 1/9: Tap + button")
            if not self._tap_element(UIElementType.MAIN_PLUS_BUTTON, delay_ms=1000):
                result.failed_step = "main_plus_button"
                return result
            result.steps_completed += 1

            # Step 2: Tap "Blog Write" menu
            logger.info("Step 2/9: Tap blog write menu")
            if not self._tap_element(UIElementType.WRITE_MENU_BLOG, delay_ms=1500):
                result.failed_step = "write_menu_blog"
                return result
            result.steps_completed += 1

            # Step 3: Input title
            logger.info(f"Step 3/9: Input title: {title[:30]}...")
            if not self._input_text_smart(title, UIElementType.TITLE_FIELD):
                result.failed_step = "title_input"
                return result
            result.steps_completed += 1

            # Step 4: Input content
            logger.info(f"Step 4/9: Input content ({len(content)} chars)")
            if not self._input_text_smart(content, UIElementType.CONTENT_FIELD):
                result.failed_step = "content_input"
                return result
            result.steps_completed += 1

            # Step 5: Adjust text size (optional)
            logger.info("Step 5/9: Adjust text size")
            # Tap text size button
            if self._tap_element(UIElementType.TEXT_SIZE_BUTTON, delay_ms=800):
                # Select smallest size
                self._tap_element(UIElementType.TEXT_SIZE_SMALLEST, delay_ms=800)
            result.steps_completed += 1

            # Step 6: Publish
            logger.info("Step 6/9: Tap publish button")
            if not self._tap_element(UIElementType.PUBLISH_BUTTON, delay_ms=2000):
                result.failed_step = "publish"
                return result
            result.steps_completed += 1

            # Step 7: Confirm (if dialog appears)
            logger.info("Step 7/9: Confirm publish")
            self._tap_element(UIElementType.CONFIRM_BUTTON, delay_ms=2000)
            result.steps_completed += 1

            # Step 8: Share
            logger.info("Step 8/9: Tap share button")
            if not self._tap_element(UIElementType.SHARE_BUTTON, delay_ms=1000):
                # Share button might not always appear - not critical
                logger.warning("Share button not clicked - continuing")
            result.steps_completed += 1

            # Step 9: Copy URL
            logger.info("Step 9/9: Copy URL")
            if self._tap_element(UIElementType.COPY_URL_BUTTON, delay_ms=1000):
                # Get URL from clipboard
                time.sleep(0.5)
                blog_url = self.adb.get_clipboard()
                result.blog_url = blog_url.strip() if blog_url else None
                logger.info(f"✅ Blog URL: {result.blog_url}")
            result.steps_completed += 1

            # Success!
            result.success = True
            result.execution_time = time.time() - self.start_time

            logger.info(
                f"🎉 Posting completed in {result.execution_time:.2f}s - URL: {result.blog_url}"
            )

        except Exception as e:
            logger.error(f"❌ Posting failed: {e}")
            result.error_message = str(e)
            result.execution_time = time.time() - self.start_time if self.start_time else 0

        return result

    async def execute_posting_with_retry(
        self,
        title: str,
        content: str,
        images: Optional[List[str]] = None,
    ) -> PostingResult:
        """
        Execute posting with retry logic

        Retries entire sequence up to max_retries times

        Args:
            title: Blog post title
            content: Blog post content
            images: Optional image paths

        Returns:
            PostingResult
        """
        last_result = None

        for attempt in range(1, self.max_retries + 1):
            logger.info(f"📝 Posting attempt {attempt}/{self.max_retries}")

            result = await self.execute_posting(title, content, images)

            if result.success:
                return result

            logger.warning(
                f"Attempt {attempt} failed at step {result.failed_step}. "
                f"Completed: {result.steps_completed}/{result.total_steps}"
            )

            last_result = result

            # Wait before retry
            if attempt < self.max_retries:
                time.sleep(3)

        # All retries failed
        logger.error(f"❌ All {self.max_retries} attempts failed")
        return last_result


# ============================================================================
# Helper Functions
# ============================================================================

def create_automator(
    device_id: str,
    profile_id: str,
    db: Session,
) -> BlogPostingAutomator:
    """
    Factory function to create automation executor

    Args:
        device_id: ADB device serial
        profile_id: Device profile ID
        db: Database session

    Returns:
        BlogPostingAutomator instance
    """
    return BlogPostingAutomator(device_id, profile_id, db)
