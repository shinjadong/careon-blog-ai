"""
Debug Logger Service - Automatic debugging with screenshot and log capture

Automatically saves:
- Screenshots for each calibration step
- Click coordinates and metadata
- WebSocket events
- API errors
"""
from pathlib import Path
from datetime import datetime
import json
import base64
from typing import Optional, Dict
from loguru import logger

from app.core.config import settings


class DebugLogger:
    """
    Production-grade debug logger with automatic screenshot and event capture
    """

    def __init__(self, session_id: str):
        """
        Initialize debug logger for a calibration session

        Args:
            session_id: Calibration session ID
        """
        self.session_id = session_id
        self.session_dir = self._create_session_directory()
        self.events_log = []
        self.screenshot_count = 0

    def _create_session_directory(self) -> Path:
        """Create directory for this debug session"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        session_dir = (
            settings.DATA_DIR / "debug_sessions" / f"{timestamp}_{self.session_id[:8]}"
        )
        session_dir.mkdir(parents=True, exist_ok=True)

        # Create subdirectories
        (session_dir / "screenshots").mkdir(exist_ok=True)
        (session_dir / "logs").mkdir(exist_ok=True)

        logger.info(f"Created debug session directory: {session_dir}")
        return session_dir

    def log_event(
        self,
        event_type: str,
        data: Dict,
        save_screenshot: bool = False,
        screenshot_b64: Optional[str] = None,
    ):
        """
        Log a calibration event

        Args:
            event_type: Type of event (click, error, websocket, etc.)
            data: Event data dictionary
            save_screenshot: Whether to save screenshot
            screenshot_b64: Base64 encoded screenshot
        """
        timestamp = datetime.now().isoformat()

        event = {
            "timestamp": timestamp,
            "event_type": event_type,
            "data": data,
        }

        # Save screenshot if provided
        if save_screenshot and screenshot_b64:
            screenshot_path = self._save_screenshot(screenshot_b64, event_type)
            event["screenshot"] = str(screenshot_path)

        self.events_log.append(event)

        # Write to log file
        self._write_event_log(event)

        logger.debug(f"Debug event logged: {event_type}")

    def _save_screenshot(self, screenshot_b64: str, event_type: str) -> Path:
        """
        Save screenshot to disk

        Args:
            screenshot_b64: Base64 encoded screenshot
            event_type: Event type for filename

        Returns:
            Path to saved screenshot
        """
        self.screenshot_count += 1
        timestamp = datetime.now().strftime("%H%M%S")
        filename = f"{self.screenshot_count:03d}_{timestamp}_{event_type}.png"
        filepath = self.session_dir / "screenshots" / filename

        # Decode and save
        screenshot_bytes = base64.b64decode(screenshot_b64)
        filepath.write_bytes(screenshot_bytes)

        logger.debug(f"Screenshot saved: {filepath}")
        return filepath

    def _write_event_log(self, event: Dict):
        """
        Write event to log file

        Args:
            event: Event dictionary
        """
        log_file = self.session_dir / "logs" / "events.jsonl"

        with open(log_file, "a") as f:
            f.write(json.dumps(event, ensure_ascii=False) + "\n")

    def log_click(
        self,
        step: int,
        element_name: str,
        x: int,
        y: int,
        screenshot_b64: Optional[str] = None,
    ):
        """Log a calibration click event"""
        self.log_event(
            "click",
            {
                "step": step,
                "element_name": element_name,
                "coordinates": {"x": x, "y": y},
            },
            save_screenshot=True,
            screenshot_b64=screenshot_b64,
        )

    def log_error(self, error_type: str, error_message: str, stack_trace: Optional[str] = None):
        """Log an error event"""
        self.log_event(
            "error",
            {
                "error_type": error_type,
                "message": error_message,
                "stack_trace": stack_trace,
            },
        )

    def log_websocket_event(self, event_type: str, message: str):
        """Log WebSocket event"""
        self.log_event(
            "websocket",
            {
                "event": event_type,
                "message": message,
            },
        )

    def finalize_session(self, success: bool, total_steps: int, completed_steps: int):
        """
        Finalize debug session and create summary report

        Args:
            success: Whether calibration completed successfully
            total_steps: Total number of steps
            completed_steps: Number of completed steps
        """
        summary = {
            "session_id": self.session_id,
            "success": success,
            "total_steps": total_steps,
            "completed_steps": completed_steps,
            "total_events": len(self.events_log),
            "screenshots_saved": self.screenshot_count,
            "session_directory": str(self.session_dir),
            "timestamp": datetime.now().isoformat(),
        }

        # Save summary
        summary_file = self.session_dir / "summary.json"
        summary_file.write_text(json.dumps(summary, indent=2, ensure_ascii=False))

        # Save full event log
        full_log_file = self.session_dir / "logs" / "full_session.json"
        full_log_file.write_text(
            json.dumps(self.events_log, indent=2, ensure_ascii=False)
        )

        logger.info(
            f"Debug session finalized: {completed_steps}/{total_steps} steps - {summary_file}"
        )

        return summary


# Global storage for active debug sessions
_active_debug_sessions: Dict[str, DebugLogger] = {}


def get_debug_logger(session_id: str) -> DebugLogger:
    """
    Get or create debug logger for session

    Args:
        session_id: Calibration session ID

    Returns:
        DebugLogger instance
    """
    if session_id not in _active_debug_sessions:
        _active_debug_sessions[session_id] = DebugLogger(session_id)

    return _active_debug_sessions[session_id]


def remove_debug_logger(session_id: str):
    """Remove debug logger from active sessions"""
    if session_id in _active_debug_sessions:
        del _active_debug_sessions[session_id]
