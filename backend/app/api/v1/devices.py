"""
Device Management API Endpoints
"""
from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from typing import List
from loguru import logger

from app.core.database import get_db
from app.services.device_manager import DeviceManager
from app.services.adb_controller import ADBController
from app.schemas.device import (
    DeviceInfo,
    DeviceProfileResponse,
    DeviceListResponse,
    DeviceProfileUpdate,
    DeviceConnectionStatus,
)
from app.schemas.coordinate import (
    CoordinateResponse,
    CoordinateCreate,
    CoordinateUpdate,
    CoordinateListResponse,
)

router = APIRouter()


@router.get("/scan", response_model=List[DeviceInfo])
async def scan_devices(db: Session = Depends(get_db)):
    """
    Scan for connected ADB devices

    Returns list of all connected devices with their information
    """
    try:
        manager = DeviceManager(db)
        devices = manager.scan_devices()

        if not devices:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No ADB devices found. Please check USB connection and ensure USB debugging is enabled.",
            )

        return devices

    except Exception as e:
        logger.error(f"Device scan failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to scan devices: {str(e)}",
        )


@router.post("/connect/{device_id}", response_model=DeviceProfileResponse)
async def connect_device(device_id: str, db: Session = Depends(get_db)):
    """
    Connect to specific device and create/update profile

    Creates new profile if device specs are new, or updates existing profile
    """
    try:
        # Create ADB controller for this device
        controller = ADBController(device_id)
        if not controller.connect():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to connect to device: {device_id}",
            )

        # Get device info
        device_info = controller.get_device_info()

        # Get or create profile
        manager = DeviceManager(db)
        profile = manager.get_or_create_profile(device_info)

        # Get coordinate count
        coords = manager.get_coordinates(profile.profile_id)
        response_data = profile.to_dict()
        response_data["coordinate_count"] = len(coords)

        return response_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to connect device: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to connect device: {str(e)}",
        )


@router.get("/profiles", response_model=DeviceListResponse)
async def list_profiles(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """
    List all device profiles with pagination

    Query Parameters:
    - skip: Number of records to skip (default: 0)
    - limit: Maximum number of records (default: 100)
    """
    try:
        manager = DeviceManager(db)
        profiles, total = manager.list_profiles(skip=skip, limit=limit)

        # Convert to response format
        profiles_data = []
        for profile in profiles:
            data = profile.to_dict()
            coords = manager.get_coordinates(profile.profile_id)
            data["coordinate_count"] = len(coords)
            profiles_data.append(data)

        return {"total": total, "devices": profiles_data}

    except Exception as e:
        logger.error(f"Failed to list profiles: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list profiles: {str(e)}",
        )


@router.get("/profiles/{profile_id}", response_model=DeviceProfileResponse)
async def get_profile(profile_id: str, db: Session = Depends(get_db)):
    """Get specific device profile by ID"""
    try:
        manager = DeviceManager(db)
        profile = manager.get_profile(profile_id)

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile not found: {profile_id}",
            )

        # Add coordinate count
        coords = manager.get_coordinates(profile_id)
        response_data = profile.to_dict()
        response_data["coordinate_count"] = len(coords)

        return response_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get profile: {str(e)}",
        )


@router.patch("/profiles/{profile_id}", response_model=DeviceProfileResponse)
async def update_profile(
    profile_id: str,
    update_data: DeviceProfileUpdate,
    db: Session = Depends(get_db),
):
    """Update device profile"""
    try:
        manager = DeviceManager(db)
        profile = manager.update_profile(profile_id, update_data)

        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile not found: {profile_id}",
            )

        # Add coordinate count
        coords = manager.get_coordinates(profile_id)
        response_data = profile.to_dict()
        response_data["coordinate_count"] = len(coords)

        return response_data

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update profile: {str(e)}",
        )


@router.delete("/profiles/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(profile_id: str, db: Session = Depends(get_db)):
    """Delete device profile and all associated coordinates"""
    try:
        manager = DeviceManager(db)
        success = manager.delete_profile(profile_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile not found: {profile_id}",
            )

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete profile: {str(e)}",
        )


# Coordinate Management Endpoints

@router.get("/profiles/{profile_id}/coordinates", response_model=CoordinateListResponse)
async def get_coordinates(profile_id: str, db: Session = Depends(get_db)):
    """Get all coordinate configurations for a profile"""
    try:
        manager = DeviceManager(db)

        # Check if profile exists
        profile = manager.get_profile(profile_id)
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Profile not found: {profile_id}",
            )

        coords = manager.get_coordinates(profile_id)
        coords_data = [coord.to_dict() for coord in coords]

        return {"total": len(coords_data), "coordinates": coords_data}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to get coordinates: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get coordinates: {str(e)}",
        )


@router.post("/coordinates", response_model=CoordinateResponse, status_code=status.HTTP_201_CREATED)
async def create_coordinate(
    coord_data: CoordinateCreate,
    db: Session = Depends(get_db),
):
    """Create new coordinate configuration"""
    try:
        manager = DeviceManager(db)
        coord = manager.create_coordinate(coord_data)

        if not coord:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Failed to create coordinate",
            )

        return coord.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to create coordinate: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create coordinate: {str(e)}",
        )


@router.patch("/coordinates/{coord_id}", response_model=CoordinateResponse)
async def update_coordinate(
    coord_id: int,
    update_data: CoordinateUpdate,
    db: Session = Depends(get_db),
):
    """Update coordinate configuration"""
    try:
        manager = DeviceManager(db)
        coord = manager.update_coordinate(coord_id, update_data)

        if not coord:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Coordinate not found: {coord_id}",
            )

        return coord.to_dict()

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to update coordinate: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update coordinate: {str(e)}",
        )


@router.delete("/coordinates/{coord_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_coordinate(coord_id: int, db: Session = Depends(get_db)):
    """Delete coordinate configuration"""
    try:
        manager = DeviceManager(db)
        success = manager.delete_coordinate(coord_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Coordinate not found: {coord_id}",
            )

        return Response(status_code=status.HTTP_204_NO_CONTENT)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete coordinate: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete coordinate: {str(e)}",
        )


@router.get("/{device_id}/screenshot")
async def get_screenshot(device_id: str):
    """
    Capture real-time screenshot from device

    Returns base64 encoded image
    """
    try:
        controller = ADBController(device_id)
        if not controller.connect():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Failed to connect to device: {device_id}",
            )

        screenshot_b64 = controller.screenshot_base64(quality=80)

        return {
            "device_id": device_id,
            "screenshot": screenshot_b64,
            "format": "png",
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Screenshot failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to capture screenshot: {str(e)}",
        )
