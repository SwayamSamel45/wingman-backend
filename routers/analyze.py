from fastapi import APIRouter, HTTPException
from models.schemas import (
    AnalyzeRequest,
    AnalyzeResponse,
    SuggestedReply,
    ErrorResponse
)
from services.gemini_service import analyze_screenshot

router = APIRouter(prefix="/api", tags=["analyze"])


@router.post(
    "/analyze",
    response_model=AnalyzeResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        500: {"model": ErrorResponse, "description": "Server error"}
    }
)
async def analyze_conversation(request: AnalyzeRequest):
    """
    Analyze a text conversation screenshot and provide coaching advice.
    
    - **image_base64**: Base64-encoded screenshot image
    - **tone**: Desired reply tone (playful, confident, mysterious, direct)
    - **risk_level**: How bold the replies should be (safe, medium, bold)
    - **platform**: Messaging platform (instagram, hinge, whatsapp, etc.)
    """
    try:
        # Validate image data
        if not request.image_base64:
            raise HTTPException(status_code=400, detail="Image data is required")
        
        # Call OpenAI Vision API
        result = await analyze_screenshot(
            image_base64=request.image_base64,
            tone=request.tone,
            risk_level=request.risk_level,
            platform=request.platform
        )
        
        # Parse suggested replies
        suggested_replies = [
            SuggestedReply(
                text=reply.get("text", ""),
                why_it_works=reply.get("why_it_works", "")
            )
            for reply in result.get("suggested_replies", [])
        ]
        
        # Build response
        response = AnalyzeResponse(
            interest_score=result.get("interest_score", 50),
            interest_status=result.get("interest_status", "Warming"),
            situation_analysis=result.get("situation_analysis", "Unable to analyze"),
            why_last_didnt_work=result.get("why_last_didnt_work"),
            diagnosis=result.get("diagnosis", "Unknown"),
            suggested_replies=suggested_replies,
            texting_principle=result.get("texting_principle", "Match their energy")
        )
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
