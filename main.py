from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import settings
from routers.analyze import router as analyze_router

# Create FastAPI app
app = FastAPI(
    title="Wingman API",
    description="AI-powered texting coach that analyzes conversation screenshots and provides coaching advice",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(analyze_router)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "app": "Wingman",
        "description": "AI-powered texting coach",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint for deployment monitoring"""
    return {"status": "healthy"}
