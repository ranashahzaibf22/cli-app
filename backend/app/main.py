"""StyleSense.AI FastAPI Application"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.config import get_settings
from app.database import Base, engine
from app.routes import auth, products

settings = get_settings()

# Create tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app
app = FastAPI(
    title="StyleSense.AI API",
    description="Virtual Fashion Try-On Platform with ML and AR",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS middleware
origins = settings.CORS_ORIGINS.split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Mount static files
try:
    app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
except Exception:
    pass  # Directory might not exist yet

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(products.router, prefix="/api/v1/products", tags=["Products"])


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "StyleSense.AI API",
        "version": "1.0.0",
        "docs": "/api/docs"
    }


@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "stylesense-api"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
