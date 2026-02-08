# FlutterFlow Integration Guide

Connect your FlutterFlow app to the Wingman API.

## Prerequisites

- FlutterFlow account
- Deployed Wingman API (Railway/Vercel)
- Your API URL (e.g., `https://wingman-api.railway.app`)

---

## Step 1: Create API Call

1. Go to **API Calls** in FlutterFlow
2. Click **Add API Call**
3. Configure:
   - **Name**: `analyzeConversation`
   - **Method**: `POST`
   - **API URL**: `https://your-api-url.railway.app/api/analyze`

---

## Step 2: Request Body

Set **Body** to JSON:

```json
{
  "image_base64": "[image_data]",
  "tone": "playful",
  "risk_level": "medium",
  "platform": "instagram"
}
```

Map `[image_data]` to your image picker's base64 output.

---

## Step 3: Headers

Add header:
- `Content-Type`: `application/json`

---

## Step 4: Response Handling

The API returns:

```json
{
  "interest_score": 65,
  "interest_status": "Warming",
  "situation_analysis": "She's responding but keeping it short...",
  "diagnosis": "Dry replies",
  "suggested_replies": [
    {"text": "Reply 1", "why_it_works": "Explanation"},
    {"text": "Reply 2", "why_it_works": "Explanation"},
    {"text": "Reply 3", "why_it_works": "Explanation"}
  ],
  "texting_principle": "Match their energy..."
}
```

In FlutterFlow:
1. Create **App State Variables** for each field
2. Map API response to these variables
3. Display in your UI widgets

---

## Step 5: Image Upload Flow

1. Add **ImagePicker** widget
2. On image selected → Convert to Base64
3. Store in App State variable
4. Trigger API call with the base64 data

---

## Tone & Risk Options

**Tone values**: `playful`, `confident`, `mysterious`, `direct`

**Risk levels**: `safe`, `medium`, `bold`

Create dropdown widgets to let users select these.

---

## Testing

1. Run your app in preview mode
2. Upload a test screenshot
3. Verify response displays correctly

For issues, check the API health: `GET https://your-api-url/health`
