import base64
import json
import re
import google.generativeai as genai
from config import settings
from models.schemas import TonePreference, RiskLevel

# Wingman system prompt
WINGMAN_SYSTEM_PROMPT = """You are Wingman, an AI-powered texting coach.

Your purpose is to help users improve their flirting, confidence, and conversational skills while texting — not to provide generic pickup lines.

The user has uploaded a SCREENSHOT of a text conversation from platforms like Instagram, Hinge, or WhatsApp.

You must:
1. Extract the conversation from the screenshot.
   - Identify which messages belong to the user (typically on the right/blue) and which belong to the other person (typically on the left/gray).
   - Preserve message order and tone.

2. Analyze the conversation for:
   - Interest level of the other person (0–100)
   - Reply effort comparison (user vs other person)
   - Dry or low-effort replies
   - Momentum (improving, stagnant, or declining)

3. Diagnose the situation using ONE primary label:
   - Dry replies
   - Over-investing
   - Good momentum
   - Needs topic switch
   - Ready to escalate

4. Coach the user instead of replacing their personality.
   - Avoid desperation
   - Avoid over-complimenting
   - Avoid long paragraphs
   - Avoid cringe or try-hard behavior

RULES FOR REPLIES:
- Max 20 words each
- Natural, human, confident
- No emojis unless platform is Instagram
- No compliments unless interest score is above 60
- No neediness or validation-seeking

You MUST respond in this EXACT JSON format (no markdown, no extra text):
{
    "interest_score": <0-100>,
    "interest_status": "<Cold | Warming | Engaged>",
    "situation_analysis": "<Clear 1-2 sentence explanation of the current dynamic>",
    "why_last_didnt_work": "<Short explanation focused on texting principles, or null if N/A>",
    "diagnosis": "<Dry replies | Over-investing | Good momentum | Needs topic switch | Ready to escalate>",
    "suggested_replies": [
        {"text": "<Reply 1>", "why_it_works": "<Explanation>"},
        {"text": "<Reply 2>", "why_it_works": "<Explanation>"},
        {"text": "<Reply 3>", "why_it_works": "<Explanation>"}
    ],
    "texting_principle": "<One general rule the user should learn>"
}"""


def get_tone_instruction(tone: TonePreference, risk_level: RiskLevel) -> str:
    """Generate additional instructions based on tone and risk level"""
    tone_instructions = {
        TonePreference.PLAYFUL: "Make the replies playful and teasing, with light humor.",
        TonePreference.CONFIDENT: "Make the replies self-assured and direct, showing high value.",
        TonePreference.MYSTERIOUS: "Make the replies intriguing and leave things to curiosity.",
        TonePreference.DIRECT: "Make the replies straightforward and to the point.",
    }
    
    risk_instructions = {
        RiskLevel.SAFE: "Keep replies safe and non-risky. Avoid anything that could backfire.",
        RiskLevel.MEDIUM: "Balance between safe and bold. Some calculated risks are okay.",
        RiskLevel.BOLD: "Be bold and daring. Push boundaries while staying confident.",
    }
    
    return f"\n\nTONE: {tone_instructions.get(tone, '')}\nRISK LEVEL: {risk_instructions.get(risk_level, '')}"


async def analyze_screenshot(
    image_base64: str,
    tone: TonePreference = TonePreference.PLAYFUL,
    risk_level: RiskLevel = RiskLevel.MEDIUM,
    platform: str | None = None
) -> dict:
    """
    Analyze a conversation screenshot using Gemini Vision
    
    Args:
        image_base64: Base64-encoded image data
        tone: Desired tone for suggested replies
        risk_level: How bold the suggestions should be
        platform: The messaging platform (instagram, hinge, whatsapp, etc.)
    
    Returns:
        Structured analysis response as dictionary
    """
    
    # Clean base64 string (remove data URL prefix if present)
    if "," in image_base64:
        image_base64 = image_base64.split(",")[1]
    
    # Build the prompt with tone/risk instructions
    user_prompt = "Analyze this text conversation screenshot and provide coaching advice."
    user_prompt += get_tone_instruction(tone, risk_level)
    
    if platform:
        user_prompt += f"\n\nPLATFORM: {platform}"
        if platform.lower() == "instagram":
            user_prompt += " (emojis are acceptable on Instagram)"
    
    # Configure Gemini API key
    genai.configure(api_key=settings.GEMINI_API_KEY)
    
    # Initialize the model
    model = genai.GenerativeModel(
        model_name=settings.GEMINI_MODEL,
        system_instruction=WINGMAN_SYSTEM_PROMPT
    )
    
    # Decode base64 image
    image_bytes = base64.b64decode(image_base64)
    
    # Create the image part for Gemini
    image_part = {
        "mime_type": "image/jpeg",
        "data": image_bytes
    }
    
    # Retry with exponential backoff for rate limits
    import asyncio
    max_retries = 3
    
    for attempt in range(max_retries):
        try:
            # Generate response
            response = model.generate_content(
                [user_prompt, image_part],
                generation_config=genai.GenerationConfig(
                    temperature=0.7,
                    max_output_tokens=1000,
                )
            )
            
            # Extract and parse the response
            content = response.text
            
            # Try to extract JSON from the response
            # Sometimes the model wraps it in markdown code blocks
            json_match = re.search(r'\{[\s\S]*\}', content)
            if json_match:
                result = json.loads(json_match.group())
                return result
            else:
                raise ValueError("No valid JSON found in response")
                
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse AI response as JSON: {str(e)}")
        except Exception as e:
            error_str = str(e)
            if "429" in error_str or "quota" in error_str.lower() or "rate" in error_str.lower():
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 15  # 15s, 30s, 45s
                    await asyncio.sleep(wait_time)
                    continue
                else:
                    raise Exception(
                        "Gemini API rate limit reached. The free tier has limited requests per minute. "
                        "Please wait 60 seconds and try again."
                    )
            raise Exception(f"Analysis failed: {error_str}")

