"""
Automation API Endpoints - Automated Blog Posting
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from loguru import logger
from datetime import datetime

from app.core.database import get_db
from app.services.automation_executor import create_automator
from app.schemas.automation import PostingRequest, PostingResponse

router = APIRouter()


@router.post("/execute", response_model=PostingResponse)
async def execute_automated_posting(
    request: PostingRequest,
    db: Session = Depends(get_db),
):
    """
    Execute automated blog posting sequence

    Performs 12-step automation:
    1. + button → 2. Blog write → 3. Title → 4. Content
    5. Text size → 6. Publish → 7-9. Share & URL

    Returns blog URL if successful
    """
    try:
        logger.info(
            f"🤖 Starting automated posting: {request.title[:30]}... on {request.device_id}"
        )

        # Create automator
        automator = create_automator(
            device_id=request.device_id,
            profile_id=request.profile_id,
            db=db,
        )

        # Execute posting with retry
        result = await automator.execute_posting_with_retry(
            title=request.title,
            content=request.content,
            images=request.images,
        )

        # Convert to response
        response = PostingResponse(
            success=result.success,
            blog_url=result.blog_url,
            error_message=result.error_message,
            steps_completed=result.steps_completed,
            total_steps=result.total_steps,
            execution_time=result.execution_time,
            failed_step=result.failed_step,
            timestamp=datetime.utcnow().isoformat(),
        )

        if result.success:
            logger.info(f"✅ Posting successful: {result.blog_url}")
        else:
            logger.error(
                f"❌ Posting failed at step: {result.failed_step} - {result.error_message}"
            )

        return response

    except ValueError as e:
        logger.error(f"Invalid request: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        logger.error(f"Automation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Automation failed: {str(e)}",
        )
