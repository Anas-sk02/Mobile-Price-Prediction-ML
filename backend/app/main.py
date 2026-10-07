"""
SmartPrice — FastAPI Backend Application
=========================================
Main entrypoint configuring CORS, application lifespan, and endpoint routers.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .predictor import engine
from .routes import health, predict, models, analytics


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Load ML models and preprocessor pipeline
    print("Starting up SmartPrice API Engine...")
    engine.load()
    print("Models loaded and ready for predictions.")
    yield
    # Shutdown
    print("Shutting down SmartPrice API Engine.")


app = FastAPI(
    title="SmartPrice API",
    description="Machine Learning API for Smartphone Price Category Prediction & Multi-Model Benchmarking",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS Middleware for Next.js / React Frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permits all origins for dev/production integration
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from pathlib import Path
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Mount Routers under /api
app.include_router(health.router, prefix="/api")
app.include_router(predict.router, prefix="/api")
app.include_router(models.router, prefix="/api")
app.include_router(analytics.router, prefix="/api")

# Serve Frontend static assets in Production if built
frontend_dist = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"

if frontend_dist.exists() and (frontend_dist / "index.html").exists():
    if (frontend_dist / "assets").exists():
        app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str = ""):
        # Fallback to index.html for SPA client-side routing
        file_path = frontend_dist / full_path
        if full_path and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(frontend_dist / "index.html"))
else:
    @app.get("/")
    def root():
        return {
            "message": "Welcome to SmartPrice ML Prediction API",
            "docs": "/docs",
            "health": "/api/health"
        }
