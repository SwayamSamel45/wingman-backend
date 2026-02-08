"""
Wingman API Test Script
-----------------------
Tests the /api/analyze endpoint with a sample screenshot.

Usage:
    1. Place a screenshot named 'test_screenshot.png' in this folder
    2. Run: python test_api.py
"""

import base64
import requests
import sys
from pathlib import Path


def test_analyze(image_path: str = "test_screenshot.png"):
    """Test the Wingman analyze endpoint"""
    
    # Check if image exists
    if not Path(image_path).exists():
        print(f"❌ Error: Image not found at '{image_path}'")
        print("\n📸 Please save a text conversation screenshot as 'test_screenshot.png'")
        print("   in the same folder as this script.")
        return
    
    # Read and encode image
    print(f"📷 Loading image: {image_path}")
    with open(image_path, "rb") as f:
        image_base64 = base64.b64encode(f.read()).decode()
    
    print(f"📤 Sending to Wingman API...")
    
    # Make request
    try:
        response = requests.post(
            "http://localhost:8000/api/analyze",
            json={
                "image_base64": image_base64,
                "tone": "playful",
                "risk_level": "medium",
                "platform": "instagram"
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            print("\n" + "="*50)
            print("🎯 WINGMAN ANALYSIS")
            print("="*50)
            
            # Interest Score
            score = result.get("interest_score", 0)
            status = result.get("interest_status", "Unknown")
            print(f"\n💓 Interest Level: {score}/100 — {status}")
            
            # Diagnosis
            print(f"\n🔍 Diagnosis: {result.get('diagnosis', 'N/A')}")
            
            # Situation
            print(f"\n📊 What's Going On:")
            print(f"   {result.get('situation_analysis', 'N/A')}")
            
            # Why last didn't work
            if result.get("why_last_didnt_work"):
                print(f"\n⚠️  Why Last Message Didn't Work:")
                print(f"   {result['why_last_didnt_work']}")
            
            # Suggested Replies
            print(f"\n💬 Better Replies:")
            for i, reply in enumerate(result.get("suggested_replies", []), 1):
                print(f"\n   {i}. \"{reply.get('text', '')}\"")
                print(f"      Why it works: {reply.get('why_it_works', '')}")
            
            # Texting Principle
            print(f"\n📚 Texting Principle:")
            print(f"   {result.get('texting_principle', 'N/A')}")
            
            print("\n" + "="*50)
            
        else:
            print(f"\n❌ Error {response.status_code}:")
            print(response.json())
            
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to API!")
        print("   Make sure the server is running:")
        print("   uvicorn main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    # Use command line argument if provided
    image_path = sys.argv[1] if len(sys.argv) > 1 else "test_screenshot.png"
    test_analyze(image_path)
