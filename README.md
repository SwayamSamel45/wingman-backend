# Wingman Backend

AI-powered texting coach API using FastAPI and OpenAI GPT-4o Vision.

## Setup

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file:
```
OPENAI_API_KEY=your_openai_api_key
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_anon_key
```

## Run Locally

```bash
uvicorn main:app --reload
```

## API Endpoints

- `POST /api/analyze` - Analyze a screenshot conversation
- `GET /health` - Health check

## Deployment

Deploy to Railway or Vercel using the provided configuration files.
