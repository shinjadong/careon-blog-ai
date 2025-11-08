"""
Automation Pydantic Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List


class PostingRequest(BaseModel):
    """Schema for blog posting request"""

    profile_id: str = Field(..., description="Device profile ID")
    device_id: str = Field(..., description="ADB device serial")
    title: str = Field(..., min_length=1, max_length=200, description="Post title")
    content: str = Field(..., min_length=1, description="Post content")
    images: Optional[List[str]] = Field(None, description="Image file paths")


class PostingResponse(BaseModel):
    """Schema for posting result"""

    success: bool
    blog_url: Optional[str] = None
    error_message: Optional[str] = None
    steps_completed: int
    total_steps: int
    execution_time: float
    failed_step: Optional[str] = None
    timestamp: str


class AutomationStatus(BaseModel):
    """Schema for automation status"""

    running: bool
    current_step: Optional[int] = None
    total_steps: int
    progress_percentage: float
