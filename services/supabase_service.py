from supabase import create_client, Client
from config import settings
from typing import Optional
import uuid

# Initialize Supabase client (if credentials are provided)
supabase: Optional[Client] = None

if settings.SUPABASE_URL and settings.SUPABASE_KEY:
    supabase = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)


async def get_or_create_user(device_id: str) -> dict:
    """
    Get or create a user based on device ID
    
    Args:
        device_id: Unique device identifier
    
    Returns:
        User record dictionary
    """
    if not supabase:
        # Return mock user if Supabase not configured
        return {"id": str(uuid.uuid4()), "device_id": device_id}
    
    # Try to find existing user
    result = supabase.table("users").select("*").eq("device_id", device_id).execute()
    
    if result.data:
        return result.data[0]
    
    # Create new user
    new_user = supabase.table("users").insert({"device_id": device_id}).execute()
    return new_user.data[0]


async def save_analysis(
    user_id: str,
    interest_score: int,
    diagnosis: str,
    suggested_replies: list,
    texting_principle: str
) -> dict:
    """
    Save an analysis to the database
    
    Args:
        user_id: User's UUID
        interest_score: Interest level 0-100
        diagnosis: Primary diagnosis label
        suggested_replies: List of suggested reply objects
        texting_principle: The texting principle shared
    
    Returns:
        Saved analysis record
    """
    if not supabase:
        # Return mock analysis if Supabase not configured
        return {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "interest_score": interest_score,
            "diagnosis": diagnosis
        }
    
    analysis = supabase.table("analyses").insert({
        "user_id": user_id,
        "interest_score": interest_score,
        "diagnosis": diagnosis,
        "suggested_replies": suggested_replies,
        "texting_principle": texting_principle
    }).execute()
    
    return analysis.data[0]


async def get_user_analyses(user_id: str, limit: int = 10) -> list:
    """
    Get recent analyses for a user
    
    Args:
        user_id: User's UUID
        limit: Maximum number of records to return
    
    Returns:
        List of analysis records
    """
    if not supabase:
        return []
    
    result = supabase.table("analyses")\
        .select("*")\
        .eq("user_id", user_id)\
        .order("created_at", desc=True)\
        .limit(limit)\
        .execute()
    
    return result.data
