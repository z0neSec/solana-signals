"""
Solana Signal Intelligence - Backend API

FastAPI application for narrative detection and signal analysis.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import get_settings
from api.routes import router


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    logger.info("🚀 Starting Solana Signal Intelligence...")
    logger.info(f"Environment: {get_settings().environment}")

    # Run the pipeline once on startup so there is data to display
    import asyncio
    asyncio.create_task(_run_pipeline_on_startup())

    yield
    logger.info("👋 Shutting down...")


async def _run_pipeline_on_startup():
    """Background task: run the full pipeline once at startup."""
    import asyncio
    await asyncio.sleep(2)  # Give the server a moment to finish booting
    try:
        from processing.pipeline import run_full_pipeline
        result = await run_full_pipeline()
        logger.info(f"🏁 Startup pipeline finished: {result}")
    except Exception as e:
        logger.error(f"Startup pipeline failed: {e}")


app = FastAPI(
    title="Solana Signal Intelligence",
    description="Detecting emerging narratives on Solana before they're obvious",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "name": "Solana Signal Intelligence",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs"
    }


async def run_pipeline():
    """Run the full signal detection pipeline (delegates to processing.pipeline)."""
    from processing.pipeline import run_full_pipeline
    return await run_full_pipeline()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
