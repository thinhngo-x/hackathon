"""Health check and status endpoints."""

from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Health"])


@router.get("/")
async def health_check():
    """Detailed health check endpoint."""
    return {
        "status": "healthy",
        "services": {
            "report_service": True,  # Will be updated with actual service checks
            "groq_classifier": True  # Will be updated with actual service checks
        }
    }


@router.get("/ready")
async def readiness_check():
    """Readiness check for deployment."""
    return {"status": "ready"}


@router.get("/live")
async def liveness_check():
    """Liveness check for deployment."""
    return {"status": "alive"}
