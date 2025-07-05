import logging
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ticket_assistant.api import classification
from ticket_assistant.api import combined
from ticket_assistant.api import health
from ticket_assistant.api import reports
from ticket_assistant.services.groq_classifier import GroqClassifier
from ticket_assistant.services.report_service import ReportService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa: ARG001
    # Startup
    logger.info("Starting up Ticket Assistant API...")

    # Initialize services
    api_endpoint = os.getenv("TICKET_API_ENDPOINT", "https://api.example.com/tickets")
    report_service = ReportService(api_endpoint=api_endpoint)

    # Set the global service instances
    reports.report_service = report_service
    combined.report_service = report_service

    # Initialize Groq classifier (will be set up when API key is provided)
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        try:
            groq_classifier_instance = GroqClassifier(api_key=groq_api_key)
            classification.groq_classifier = groq_classifier_instance
            combined.groq_classifier = groq_classifier_instance
            logger.info("Groq classifier initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize Groq classifier: {e!s}")
    else:
        logger.warning("GROQ_API_KEY not provided, classification will use mock responses")

    yield

    # Shutdown
    logger.info("Shutting down Ticket Assistant API...")


# Create FastAPI app
app = FastAPI(
    title="Ticket Assistant API",
    description="AI-powered ticket reporting and classification system",
    version="1.0.0",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(reports.router)
app.include_router(classification.router)
app.include_router(combined.router)


@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "Ticket Assistant API is running",
        "status": "healthy",
        "groq_available": classification.groq_classifier is not None,
        "version": "1.0.0",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
    }


# Legacy dependency functions for backward compatibility
def get_report_service() -> ReportService:
    """Legacy dependency function."""
    return reports.get_report_service()


def get_groq_classifier() -> GroqClassifier:
    """Legacy dependency function."""
    return classification.get_groq_classifier()


def main():
    """Main entry point for running the application."""
    import os

    import uvicorn

    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("API_PORT", "8000"))
    debug = os.getenv("DEBUG", "True").lower() == "true"

    uvicorn.run(
        "ticket_assistant.api.main:app",
        host=host,
        port=port,
        reload=debug,
        log_level="info",
    )


if __name__ == "__main__":
    main()
