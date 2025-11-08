"""
ADB Controller Service - Production-grade Android device control

Uses adbutils for reliable ADB communication
"""
from adbutils import adb, AdbDevice, AdbError
from typing import Optional, List
from pathlib import Path
import time
import base64
from io import BytesIO
from PIL import Image
from loguru import logger

from app.core.config import settings


class ADBController:
    """
    Production-grade ADB controller with error handling and retry logic

    Handles all low-level device interactions:
    - Device discovery and connection
    - Screenshot capture
    - Touch events (tap, swipe)
    - Text input
    - Key events
    - Clipboard operations
    """

    def __init__(
        self,
        device_id: Optional[str] = None,
        timeout: int = settings.ADB_TIMEOUT,
    ):
        """
        Initialize ADB controller

        Args:
            device_id: ADB serial number (None = use first available device)
            timeout: Command timeout in seconds
        """
        self.device_id = device_id
        self.timeout = timeout
        self._device: Optional[AdbDevice] = None

    def connect(self) -> bool:
        """
        Connect to ADB device

        Returns:
            True if connection successful
        """
        try:
            if self.device_id:
                self._device = adb.device(serial=self.device_id)
            else:
                devices = adb.device_list()
                if not devices:
                    logger.error("No ADB devices found")
                    return False
                self._device = devices[0]
                self.device_id = self._device.serial

            # Test connection
            self._device.shell("echo 'connected'")
            logger.info(f"Connected to device: {self.device_id}")
            return True

        except AdbError as e:
            logger.error(f"Failed to connect to device: {e}")
            return False

    @property
    def device(self) -> AdbDevice:
        """Get connected device (auto-connect if needed)"""
        if self._device is None:
            if not self.connect():
                raise ConnectionError("Failed to connect to ADB device")
        return self._device

    def get_device_info(self) -> dict:
        """
        Get comprehensive device information

        Returns:
            Dictionary with device metadata
        """
        try:
            info = {
                "device_id": self.device_id,
                "model": self.shell("getprop ro.product.model").strip(),
                "manufacturer": self.shell("getprop ro.product.manufacturer").strip(),
                "android_version": self.shell(
                    "getprop ro.build.version.release"
                ).strip(),
                "sdk_version": self.shell(
                    "getprop ro.build.version.sdk"
                ).strip(),
                "width": 0,
                "height": 0,
                "dpi": 0,
            }

            # Get screen resolution
            wm_size = self.shell("wm size").strip()
            if "Physical size:" in wm_size:
                res = wm_size.split(": ")[1]
                width, height = res.split("x")
                info["width"] = int(width)
                info["height"] = int(height)

            # Get screen density
            wm_density = self.shell("wm density").strip()
            if "Physical density:" in wm_density:
                info["dpi"] = int(wm_density.split(": ")[1])

            return info

        except Exception as e:
            logger.error(f"Failed to get device info: {e}")
            raise

    def shell(self, command: str) -> str:
        """
        Execute ADB shell command

        Args:
            command: Shell command to execute

        Returns:
            Command output as string
        """
        try:
            output = self.device.shell(command)
            return output

        except AdbError as e:
            logger.error(f"Shell command failed: {command} - {e}")
            raise

    def screenshot(
        self,
        save_path: Optional[Path] = None,
        quality: int = settings.DEFAULT_SCREENSHOT_QUALITY,
    ) -> bytes:
        """
        Capture device screenshot

        Args:
            save_path: Optional path to save screenshot
            quality: JPEG quality (1-100)

        Returns:
            Screenshot as bytes (PNG format)
        """
        try:
            # Capture screenshot using adbutils (returns PIL Image directly)
            image = self.device.screenshot()

            # Save if path provided
            if save_path:
                save_path.parent.mkdir(parents=True, exist_ok=True)
                image.save(save_path, "PNG", quality=quality)
                logger.debug(f"Screenshot saved to {save_path}")

            # Return as bytes
            output = BytesIO()
            image.save(output, "PNG", quality=quality)
            return output.getvalue()

        except Exception as e:
            logger.error(f"Screenshot failed: {e}")
            raise

    def screenshot_base64(self, quality: int = 80) -> str:
        """
        Capture screenshot and return as base64 string

        Args:
            quality: JPEG quality (1-100)

        Returns:
            Base64 encoded screenshot
        """
        screenshot_bytes = self.screenshot(quality=quality)
        return base64.b64encode(screenshot_bytes).decode("utf-8")

    def tap(self, x: int, y: int, delay_ms: int = settings.TAP_DELAY_MS):
        """
        Perform tap at coordinates

        Args:
            x: X coordinate
            y: Y coordinate
            delay_ms: Delay after tap in milliseconds
        """
        try:
            self.shell(f"input tap {x} {y}")
            time.sleep(delay_ms / 1000.0)
            logger.debug(f"Tapped at ({x}, {y})")

        except Exception as e:
            logger.error(f"Tap failed at ({x}, {y}): {e}")
            raise

    def swipe(
        self,
        x1: int,
        y1: int,
        x2: int,
        y2: int,
        duration_ms: int = settings.SWIPE_DURATION_MS,
    ):
        """
        Perform swipe gesture

        Args:
            x1: Start X coordinate
            y1: Start Y coordinate
            x2: End X coordinate
            y2: End Y coordinate
            duration_ms: Swipe duration in milliseconds
        """
        try:
            self.shell(f"input swipe {x1} {y1} {x2} {y2} {duration_ms}")
            logger.debug(f"Swiped from ({x1}, {y1}) to ({x2}, {y2})")

        except Exception as e:
            logger.error(f"Swipe failed: {e}")
            raise

    def key_event(self, keycode: int):
        """
        Send key event

        Args:
            keycode: Android keycode (e.g., 66 for ENTER)

        Common keycodes:
            3: HOME
            4: BACK
            66: ENTER
            67: DEL
            111: ESCAPE
        """
        try:
            self.shell(f"input keyevent {keycode}")
            logger.debug(f"Sent keycode: {keycode}")

        except Exception as e:
            logger.error(f"Key event failed: {e}")
            raise

    def input_text(self, text: str):
        """
        Input text (English only via ADB)

        Args:
            text: Text to input (spaces will be replaced with %s)

        Note: For Korean/special chars, use clipboard method
        """
        try:
            # Escape spaces and special characters
            escaped_text = text.replace(" ", "%s")
            self.shell(f"input text '{escaped_text}'")
            logger.debug(f"Input text: {text}")

        except Exception as e:
            logger.error(f"Text input failed: {e}")
            raise

    def set_clipboard(self, text: str):
        """
        Set device clipboard content

        Args:
            text: Text to copy to clipboard

        Note: Requires Clipper app or Android 10+ clipboard command
        """
        try:
            # Try Android 10+ clipboard command first
            escaped_text = text.replace('"', '\\"')
            self.shell(f'cmd clipboard set "{escaped_text}"')
            logger.debug(f"Clipboard set: {text[:50]}...")

        except Exception as e:
            logger.error(f"Set clipboard failed: {e}")
            raise

    def get_clipboard(self) -> str:
        """
        Get device clipboard content

        Returns:
            Clipboard text

        Note: Requires Android 10+ or Clipper app
        """
        try:
            output = self.shell("cmd clipboard get")
            return output.strip()

        except Exception as e:
            logger.error(f"Get clipboard failed: {e}")
            return ""

    def paste(self):
        """Trigger paste action (keycode 279)"""
        self.key_event(279)  # KEYCODE_PASTE

    def launch_app(self, package_name: str, activity: Optional[str] = None):
        """
        Launch Android application

        Args:
            package_name: App package name (e.g., com.nhn.android.blog)
            activity: Optional activity name
        """
        try:
            if activity:
                self.shell(f"am start -n {package_name}/{activity}")
            else:
                # Use monkey to launch app
                self.shell(
                    f"monkey -p {package_name} -c android.intent.category.LAUNCHER 1"
                )
            logger.info(f"Launched app: {package_name}")

        except Exception as e:
            logger.error(f"Failed to launch app: {e}")
            raise

    def stop_app(self, package_name: str):
        """
        Force stop application

        Args:
            package_name: App package name
        """
        try:
            self.shell(f"am force-stop {package_name}")
            logger.info(f"Stopped app: {package_name}")

        except Exception as e:
            logger.error(f"Failed to stop app: {e}")
            raise

    def get_current_activity(self) -> str:
        """
        Get currently focused activity

        Returns:
            Activity name
        """
        try:
            output = self.shell("dumpsys window | grep mCurrentFocus")
            return output.strip()

        except Exception as e:
            logger.error(f"Failed to get current activity: {e}")
            return ""

    def disconnect(self):
        """Disconnect from device"""
        self._device = None
        logger.info(f"Disconnected from device: {self.device_id}")


def list_connected_devices() -> List[dict]:
    """
    List all connected ADB devices

    Returns:
        List of device information dictionaries
    """
    try:
        devices = adb.device_list()
        result = []

        for device in devices:
            controller = ADBController(device.serial)
            if controller.connect():
                info = controller.get_device_info()
                result.append(info)

        return result

    except Exception as e:
        logger.error(f"Failed to list devices: {e}")
        return []
