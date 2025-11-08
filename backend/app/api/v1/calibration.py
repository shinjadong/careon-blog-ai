"""
Interactive Calibration API Endpoints

User clicks on device screen in admin dashboard to configure UI coordinates
"""
from fastapi import APIRouter, Depends, HTTPException, status, WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from typing import List, Dict
from loguru import logger
from datetime import datetime
import asyncio
import json
import uuid

from app.core.database import get_db
from app.services.device_manager import DeviceManager
from app.services.adb_controller import ADBController
from app.services.debug_logger import get_debug_logger, remove_debug_logger
from app.schemas.coordinate import (
    CalibrationSession,
    CalibrationResult,
    CalibrationGuide,
    CoordinateCreate,
    CoordinateUpdate,
)
from app.models.coordinate import UIElementType, CalibrationMethod

router = APIRouter()

# In-memory storage for active calibration sessions
active_sessions: Dict[str, dict] = {}


# Calibration workflow steps
CALIBRATION_STEPS = [
    {
        "element_type": UIElementType.WRITE_BUTTON,
        "element_name": "+ 아이콘 (메인 화면)",
        "instructions": "네이버 블로그 앱 메인 화면에서 우하단 '+' 아이콘을 클릭하세요.",
        "help_text": "화면 오른쪽 하단에 있는 플러스(+) 버튼입니다. 클릭하면 메뉴가 열립니다.",
    },
    {
        "element_type": UIElementType.HOME_BUTTON,
        "element_name": "블로그 글쓰기 버튼",
        "instructions": "메뉴에서 '블로그 글쓰기' 버튼을 클릭하세요.",
        "help_text": "+ 아이콘을 누른 후 나타나는 메뉴에서 '블로그 글쓰기' 옵션을 선택합니다.",
    },
    {
        "element_type": UIElementType.TITLE_FIELD,
        "element_name": "제목 입력 필드",
        "instructions": "에디터 화면에서 '제목을 입력하세요' 영역을 클릭하세요.",
        "help_text": "에디터 상단의 제목 입력 필드입니다.",
    },
    {
        "element_type": UIElementType.CONTENT_FIELD,
        "element_name": "본문 입력 필드",
        "instructions": "에디터 화면에서 본문 입력 영역을 클릭하세요.",
        "help_text": "제목 아래의 넓은 본문 작성 영역입니다.",
    },
    {
        "element_type": UIElementType.IMAGE_BUTTON,
        "element_name": "이미지 추가 버튼",
        "instructions": "에디터 하단 툴바에서 '이미지' 추가 버튼을 클릭하세요.",
        "help_text": "보통 사진 아이콘으로 표시됩니다.",
    },
    {
        "element_type": UIElementType.TEXT_SIZE_BUTTON,
        "element_name": "텍스트 크기 버튼",
        "instructions": "에디터 하단 툴바에서 '텍스트 크기' 버튼(가 아이콘)을 클릭하세요.",
        "help_text": "텍스트 크기를 변경하는 아이콘입니다. 보통 '가' 또는 'A' 모양입니다.",
    },
    {
        "element_type": UIElementType.BOLD_BUTTON,
        "element_name": "최소 텍스트 크기 선택",
        "instructions": "텍스트 크기 팝업에서 '가장 작은 크기'를 클릭하세요.",
        "help_text": "보통 9pt 또는 가장 왼쪽의 작은 크기 옵션입니다.",
    },
    {
        "element_type": UIElementType.LINK_BUTTON,
        "element_name": "링크 추가 버튼",
        "instructions": "이미지를 선택한 상태에서 '링크 추가' 버튼을 클릭하세요.",
        "help_text": "이미지에 URL을 연결하는 링크 아이콘 버튼입니다.",
    },
    {
        "element_type": UIElementType.PUBLISH_BUTTON,
        "element_name": "발행 버튼",
        "instructions": "에디터 상단 우측의 '발행' 버튼을 클릭하세요.",
        "help_text": "글 작성 완료 후 발행하는 버튼입니다.",
    },
    {
        "element_type": UIElementType.CONFIRM_BUTTON,
        "element_name": "확인 버튼",
        "instructions": "일반적인 '확인' 버튼을 클릭하세요.",
        "help_text": "다이얼로그나 설정 화면의 확인 버튼입니다.",
    },
    {
        "element_type": UIElementType.SHARE_BUTTON,
        "element_name": "공유 버튼",
        "instructions": "발행 완료 후 '공유' 버튼을 클릭하세요.",
        "help_text": "발행된 글을 공유하는 버튼입니다.",
    },
    {
        "element_type": UIElementType.COPY_LINK_BUTTON,
        "element_name": "링크 복사 버튼",
        "instructions": "공유 메뉴에서 '링크 복사' 버튼을 클릭하세요.",
        "help_text": "블로그 포스트 URL을 복사하는 버튼입니다.",
    },
]


@router.post("/sessions", response_model=CalibrationSession)
async def start_calibration_session(
    profile_id: str,
    calibrated_by: str = "admin",
    db: Session = Depends(get_db),
):
    """
    Start new interactive calibration session

    Initializes step-by-step UI element coordinate configuration workflow
    """
    try:
        # Verify profile exists
        manager = DeviceManager(db)
        profile = manager.get_profile(profile_id)

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile not found: {profile_id}",
            )

        # Create session
        session_id = str(uuid.uuid4())
        session_data = {
            "session_id": session_id,
            "profile_id": profile_id,
            "calibrated_by": calibrated_by,
            "current_step": 0,
            "total_steps": len(CALIBRATION_STEPS),
            "completed_steps": [],
            "created_at": datetime.utcnow(),
        }

        active_sessions[session_id] = session_data

        # Get first step
        first_step = CALIBRATION_STEPS[0]

        logger.info(f"Started calibration session: {session_id} for profile {profile_id}")

        return CalibrationSession(
            session_id=session_id,
            profile_id=profile_id,
            current_step=0,
            total_steps=len(CALIBRATION_STEPS),
            element_type=first_step["element_type"].value,
            element_name=first_step["element_name"],
            instructions=first_step["instructions"],
            completed=False,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to start calibration session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to start session: {str(e)}",
        )


@router.get("/sessions/{session_id}", response_model=CalibrationSession)
async def get_calibration_session(session_id: str):
    """Get current calibration session status"""
    try:
        if session_id not in active_sessions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session not found: {session_id}",
            )

        session = active_sessions[session_id]
        current_step_idx = session["current_step"]

        if current_step_idx >= len(CALIBRATION_STEPS):
            # Session completed
            return CalibrationSession(
                session_id=session_id,
                profile_id=session["profile_id"],
                current_step=current_step_idx,
                total_steps=len(CALIBRATION_STEPS),
                element_type="completed",
                element_name="Calibration Complete",
                instructions="All UI elements have been calibrated successfully!",
                completed=True,
            )

        # Get current step
        step = CALIBRATION_STEPS[current_step_idx]

        return CalibrationSession(
            session_id=session_id,
            profile_id=session["profile_id"],
            current_step=current_step_idx,
            total_steps=len(CALIBRATION_STEPS),
            element_type=step["element_type"].value,
            element_name=step["element_name"],
            instructions=step["instructions"],
            completed=False,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get session: {str(e)}",
        )


@router.post("/sessions/{session_id}/submit", response_model=CalibrationSession)
async def submit_calibration_coordinate(
    session_id: str,
    result: CalibrationResult,
    db: Session = Depends(get_db),
):
    """
    Submit user-clicked coordinate for current step

    User clicks on device screen in admin UI, frontend sends coordinates here
    """
    try:
        if session_id not in active_sessions:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Session not found: {session_id}",
            )

        session = active_sessions[session_id]
        current_step_idx = session["current_step"]

        if current_step_idx >= len(CALIBRATION_STEPS):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Calibration already completed",
            )

        # Get current step
        step = CALIBRATION_STEPS[current_step_idx]

        # Save coordinate to database
        manager = DeviceManager(db)
        coord_data = CoordinateCreate(
            profile_id=session["profile_id"],
            element_type=step["element_type"].value,
            element_name=step["element_name"],
            element_description=step.get("help_text", ""),
            x=result.x,
            y=result.y,
            confidence=0.95,  # High confidence for user-clicked coordinates
            validated=False,  # Will be validated through actual testing
            calibration_method=CalibrationMethod.USER_CLICK.value,
            calibrated_by=session["calibrated_by"],
            touch_radius=20,
        )

        # Check if coordinate for this element already exists
        existing_coords = manager.get_coordinates(
            session["profile_id"], element_type=step["element_type"]
        )

        if existing_coords:
            # Update existing coordinate
            coord = manager.update_coordinate(
                existing_coords[0].id,
                CoordinateUpdate(
                    x=result.x,
                    y=result.y,
                    confidence=0.95,
                    validated=False,
                    calibration_method=CalibrationMethod.USER_CLICK.value,
                    calibrated_by=session["calibrated_by"],
                ),
            )
        else:
            # Create new coordinate
            coord = manager.create_coordinate(coord_data)

        if not coord:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to save coordinate",
            )

        logger.info(
            f"Saved coordinate for {step['element_name']}: ({result.x}, {result.y})"
        )

        # Debug logging
        debug_logger = get_debug_logger(session_id)
        debug_logger.log_click(
            step=current_step_idx + 1,
            element_name=step["element_name"],
            x=result.x,
            y=result.y,
            screenshot_b64=None,  # Will be captured by WebSocket
        )

        # Mark step as completed
        session["completed_steps"].append(current_step_idx)

        # Move to next step
        session["current_step"] += 1
        next_step_idx = session["current_step"]

        # Check if calibration is complete
        if next_step_idx >= len(CALIBRATION_STEPS):
            # Update profile calibration status
            from app.schemas.device import DeviceProfileUpdate

            manager.update_profile(
                session["profile_id"],
                DeviceProfileUpdate(
                    calibrated=True,
                    calibration_confidence=0.95,
                ),
            )

            logger.info(
                f"Calibration completed for profile: {session['profile_id']}"
            )

            return CalibrationSession(
                session_id=session_id,
                profile_id=session["profile_id"],
                current_step=next_step_idx,
                total_steps=len(CALIBRATION_STEPS),
                element_type="completed",
                element_name="Calibration Complete",
                instructions="모든 UI 요소 좌표 설정이 완료되었습니다!",
                completed=True,
            )

        # Return next step
        next_step = CALIBRATION_STEPS[next_step_idx]

        return CalibrationSession(
            session_id=session_id,
            profile_id=session["profile_id"],
            current_step=next_step_idx,
            total_steps=len(CALIBRATION_STEPS),
            element_type=next_step["element_type"].value,
            element_name=next_step["element_name"],
            instructions=next_step["instructions"],
            completed=False,
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to submit coordinate: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to submit coordinate: {str(e)}",
        )


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
async def cancel_calibration_session(session_id: str):
    """Cancel and remove calibration session"""
    try:
        if session_id in active_sessions:
            del active_sessions[session_id]
            logger.info(f"Cancelled calibration session: {session_id}")

        return None

    except Exception as e:
        logger.error(f"Failed to cancel session: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to cancel session: {str(e)}",
        )


@router.get("/guide", response_model=List[CalibrationGuide])
async def get_calibration_guide():
    """
    Get complete calibration workflow guide

    Returns all steps with instructions for reference
    """
    try:
        guide = []
        for idx, step in enumerate(CALIBRATION_STEPS):
            guide.append(
                CalibrationGuide(
                    step_number=idx + 1,
                    element_type=step["element_type"].value,
                    element_name=step["element_name"],
                    instructions=step["instructions"],
                    help_text=step.get("help_text"),
                )
            )

        return guide

    except Exception as e:
        logger.error(f"Failed to get calibration guide: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get guide: {str(e)}",
        )


# WebSocket for real-time screen updates during calibration
@router.websocket("/ws/{device_id}")
async def calibration_websocket(websocket: WebSocket, device_id: str):
    """
    WebSocket endpoint for real-time device screen streaming during calibration

    Streams device screenshots to frontend for interactive coordinate selection
    """
    await websocket.accept()
    logger.info(f"WebSocket connected for device: {device_id}")

    try:
        controller = ADBController(device_id)
        if not controller.connect():
            await websocket.send_json({
                "type": "error",
                "message": f"Failed to connect to device: {device_id}",
            })
            await websocket.close()
            return

        # Send initial connection success
        await websocket.send_json({
            "type": "connected",
            "device_id": device_id,
            "message": "Screen streaming started",
        })

        # Streaming loop
        while True:
            try:
                # Check for client messages (e.g., stop command)
                try:
                    data = await asyncio.wait_for(websocket.receive_text(), timeout=0.1)
                    message = json.loads(data)

                    if message.get("type") == "stop":
                        logger.info(f"Stopping screen stream for {device_id}")
                        break

                except asyncio.TimeoutError:
                    pass

                # Capture and send screenshot
                screenshot_b64 = controller.screenshot_base64(quality=70)

                await websocket.send_json({
                    "type": "screenshot",
                    "device_id": device_id,
                    "screenshot": screenshot_b64,
                    "timestamp": datetime.utcnow().isoformat(),
                })

                # Throttle to ~2 FPS for bandwidth efficiency
                await asyncio.sleep(0.5)

            except WebSocketDisconnect:
                logger.info(f"WebSocket disconnected for device: {device_id}")
                break

    except Exception as e:
        logger.error(f"WebSocket error for device {device_id}: {e}")
        try:
            await websocket.send_json({
                "type": "error",
                "message": str(e),
            })
        except:
            pass

    finally:
        try:
            await websocket.close()
        except:
            pass
        logger.info(f"WebSocket closed for device: {device_id}")
