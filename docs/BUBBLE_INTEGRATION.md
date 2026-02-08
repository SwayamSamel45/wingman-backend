# Bubble Integration Guide

Connect your Bubble app to the Wingman API.

## Prerequisites

- Bubble account (free or paid)
- Deployed Wingman API (Railway/Vercel)
- Your API URL (e.g., `https://wingman-api.railway.app`)

---

## Step 1: Install API Connector Plugin

1. Go to **Plugins** tab
2. Search for **API Connector**
3. Install it (free plugin)

---

## Step 2: Configure API

1. Open **API Connector** settings
2. Click **Add another API**
3. Name it: `Wingman`

---

## Step 3: Create Analyze Call

Click **Add another call** and configure:

- **Name**: `analyze`
- **Method**: `POST`
- **URL**: `https://your-api-url.railway.app/api/analyze`

**Headers**:
| Key | Value |
|-----|-------|
| Content-Type | application/json |

**Body (JSON)**:
```json
{
  "image_base64": "<image_data>",
  "tone": "<tone>",
  "risk_level": "<risk_level>",
  "platform": "<platform>"
}
```

Mark `image_data`, `tone`, `risk_level`, `platform` as **dynamic**.

---

## Step 4: Initialize Call

1. Fill test values:
   - `image_data`: A small test base64 string
   - `tone`: `playful`
   - `risk_level`: `medium`
   - `platform`: `instagram`

2. Click **Initialize call**
3. Bubble will detect response structure

---

## Step 5: Create Workflow

1. Add **Picture Uploader** element
2. Create workflow: **When Picture Uploader's value is changed**
3. Add action: **Plugins → Wingman - analyze**
4. Map inputs:
   - `image_data`: Picture Uploader's value (base64)
   - `tone`: Dropdown Tone's value
   - `risk_level`: Dropdown Risk's value
   - `platform`: Input Platform's value

---

## Step 6: Display Results

Create elements to show:

| Element | Data Source |
|---------|------------|
| Text (Interest) | Result's interest_score |
| Text (Status) | Result's interest_status |
| Text (Analysis) | Result's situation_analysis |
| Text (Diagnosis) | Result's diagnosis |
| Repeating Group | Result's suggested_replies |
| Text (Principle) | Result's texting_principle |

---

## Step 7: Suggested Replies Display

For the Repeating Group:
1. Type: `suggested_replies`
2. Data source: Result's suggested_replies

Inside each cell:
- Text for `Current cell's text`
- Text for `Current cell's why_it_works`

---

## Image to Base64 in Bubble

Use **Base64 Image Encoder** plugin or JavaScript:

```javascript
function(callback, image_url) {
  fetch(image_url)
    .then(res => res.blob())
    .then(blob => {
      const reader = new FileReader();
      reader.onloadend = () => callback(reader.result);
      reader.readAsDataURL(blob);
    });
}
```

---

## Testing

1. Preview your app
2. Upload a screenshot
3. Check if results appear

For issues, visit: `https://your-api-url/docs` for API documentation.
