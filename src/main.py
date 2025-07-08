"""
FastAPI main application for GitHub to Notion synchronization.
Provides webhook endpoints, monitoring, and administrative features.
"""

from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, Any, Optional
import asyncio
import uvicorn
from fastapi import FastAPI, Request, HTTPException, BackgroundTasks, Depends, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from pydantic import BaseModel
import logging

from .config import get_config
from .utils.logger import get_logger, setup_logging
from .handlers.webhook_handler import WebhookHandler, create_webhook_handler
from .services.sync_service import SyncService
from .services.github_service import GitHubService
from .services.notion_service import NotionService

# Setup logging
setup_logging()
logger = get_logger(__name__)

# Global instances
webhook_handler: Optional[WebhookHandler] = None
sync_service: Optional[SyncService] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    # Startup
    logger.info("Starting GitHub to Notion Sync application")
    
    global webhook_handler, sync_service
    
    try:
        # Initialize services
        webhook_handler = create_webhook_handler()
        sync_service = SyncService()
        
        # Validate configuration
        validation_result = await webhook_handler.validate_webhook_config()
        if not validation_result["success"]:
            logger.error("Application validation failed", extra=validation_result)
            raise RuntimeError("Invalid configuration")
        
        logger.info("Application startup completed successfully")
        
        yield
        
    except Exception as e:
        logger.error(f"Application startup failed: {e}")
        raise
    finally:
        # Shutdown
        logger.info("Application shutdown")


# Create FastAPI app
app = FastAPI(
    title="GitHub to Notion Sync",
    description="Synchronizes GitHub Projects v2 with Notion databases",
    version="1.0.0",
    lifespan=lifespan
)

# Add middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"]  # Configure appropriately for production
)


# Request/Response models
class WebhookResponse(BaseModel):
    """Webhook response model."""
    success: bool
    message: str
    delivery_id: Optional[str] = None
    event_type: Optional[str] = None
    action: Optional[str] = None
    processing_time_ms: Optional[float] = None


class SyncResponse(BaseModel):
    """Sync response model."""
    success: bool
    message: str
    total_items: Optional[int] = None
    created: Optional[int] = None
    updated: Optional[int] = None
    failed: Optional[int] = None
    duration_seconds: Optional[float] = None


class StatusResponse(BaseModel):
    """Status response model."""
    status: str
    timestamp: str
    version: str
    uptime_seconds: Optional[float] = None


class ValidationResponse(BaseModel):
    """Validation response model."""
    success: bool
    github_connection: bool
    notion_connection: bool
    field_mappings: bool
    webhook_secret_configured: bool
    errors: list = []


# Dependency to get webhook handler
def get_webhook_handler() -> WebhookHandler:
    """Get webhook handler dependency."""
    if webhook_handler is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Webhook handler not initialized"
        )
    return webhook_handler


# Dependency to get sync service
def get_sync_service() -> SyncService:
    """Get sync service dependency."""
    if sync_service is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Sync service not initialized"
        )
    return sync_service


# Webhook endpoints
@app.post("/webhook", response_model=WebhookResponse)
async def handle_webhook(
    request: Request,
    handler: WebhookHandler = Depends(get_webhook_handler)
):
    """Handle GitHub webhook events."""
    try:
        # Special handling for ping events
        event_type = request.headers.get("X-GitHub-Event")
        if event_type == "ping":
            result = await handler.handle_ping(request)
            return WebhookResponse(
                success=True,
                message="Webhook ping received",
                delivery_id=request.headers.get("X-GitHub-Delivery"),
                event_type="ping"
            )
        
        # Handle regular webhook events
        result = await handler.handle_webhook(request)
        
        return WebhookResponse(
            success=result["success"],
            message=result.get("error", "Webhook processed successfully"),
            delivery_id=result.get("delivery_id"),
            event_type=result.get("event_type"),
            action=result.get("action"),
            processing_time_ms=result.get("processing_time_ms")
        )
        
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Unexpected error in webhook endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )


# Sync endpoints
@app.post("/sync/full", response_model=SyncResponse)
async def trigger_full_sync(
    background_tasks: BackgroundTasks,
    batch_size: Optional[int] = None,
    service: SyncService = Depends(get_sync_service)
):
    """Trigger a full synchronization."""
    try:
        # Run sync in background
        async def run_sync():
            try:
                result = await service.full_sync(batch_size)
                logger.info("Full sync completed", extra=result)
            except Exception as e:
                logger.error(f"Full sync failed: {e}")
        
        background_tasks.add_task(run_sync)
        
        return SyncResponse(
            success=True,
            message="Full sync started in background"
        )
        
    except Exception as e:
        logger.error(f"Error starting full sync: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start full sync"
        )


@app.post("/sync/cleanup", response_model=SyncResponse)
async def trigger_cleanup(
    background_tasks: BackgroundTasks,
    service: SyncService = Depends(get_sync_service)
):
    """Trigger cleanup of orphaned Notion pages."""
    try:
        async def run_cleanup():
            try:
                result = await service.cleanup_orphaned_pages()
                logger.info("Cleanup completed", extra=result)
            except Exception as e:
                logger.error(f"Cleanup failed: {e}")
        
        background_tasks.add_task(run_cleanup)
        
        return SyncResponse(
            success=True,
            message="Cleanup started in background"
        )
        
    except Exception as e:
        logger.error(f"Error starting cleanup: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to start cleanup"
        )


# Status and monitoring endpoints
@app.get("/health", response_model=StatusResponse)
async def health_check():
    """Health check endpoint."""
    return StatusResponse(
        status="healthy",
        timestamp=datetime.utcnow().isoformat(),
        version="1.0.0"
    )


@app.get("/status", response_model=Dict[str, Any])
async def get_status(
    handler: WebhookHandler = Depends(get_webhook_handler),
    service: SyncService = Depends(get_sync_service)
):
    """Get detailed application status."""
    try:
        webhook_stats = handler.get_webhook_stats()
        sync_status = service.get_sync_status()
        
        return {
            "status": "running",
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "webhook_stats": webhook_stats,
            "sync_status": sync_status
        }
        
    except Exception as e:
        logger.error(f"Error getting status: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get status"
        )


@app.get("/validate", response_model=ValidationResponse)
async def validate_configuration(
    handler: WebhookHandler = Depends(get_webhook_handler)
):
    """Validate application configuration."""
    try:
        validation_result = await handler.validate_webhook_config()
        
        return ValidationResponse(
            success=validation_result["success"],
            github_connection=validation_result.get("sync_service_ready", False),
            notion_connection=validation_result.get("sync_service_ready", False),
            field_mappings=validation_result.get("sync_service_ready", False),
            webhook_secret_configured=validation_result["webhook_secret_configured"],
            errors=validation_result["errors"]
        )
        
    except Exception as e:
        logger.error(f"Error validating configuration: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to validate configuration"
        )


# Administrative endpoints
@app.post("/admin/reset-stats")
async def reset_stats(
    handler: WebhookHandler = Depends(get_webhook_handler)
):
    """Reset webhook statistics."""
    try:
        handler.reset_stats()
        return {"success": True, "message": "Statistics reset successfully"}
        
    except Exception as e:
        logger.error(f"Error resetting stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reset statistics"
        )


@app.get("/admin/config")
async def get_config():
    """Get configuration (sanitized)."""
    try:
        config = get_config()
        settings = config.settings
        
        # Return sanitized configuration
        return {
            "github_org": settings.github_org,
            "github_project_number": settings.github_project_number,
            "notion_db_id": settings.notion_db_id,
            "batch_size": settings.batch_size,
            "environment": settings.environment,
            "log_level": settings.log_level,
            "field_mappings_count": len(config.field_mappings),
            "webhook_events_count": len(config.webhook_events),
            "has_github_token": bool(settings.github_token),
            "has_notion_token": bool(settings.notion_token),
            "has_webhook_secret": bool(settings.webhook_secret)
        }
        
    except Exception as e:
        logger.error(f"Error getting config: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get configuration"
        )


# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    logger.warning(f"HTTP {exc.status_code} error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "timestamp": datetime.utcnow().isoformat()}
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )


# Root endpoint
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "GitHub to Notion Sync API",
        "version": "1.0.0",
        "endpoints": {
            "webhook": "/webhook",
            "health": "/health",
            "status": "/status",
            "validate": "/validate",
            "full_sync": "/sync/full",
            "cleanup": "/sync/cleanup",
            "docs": "/docs"
        }
    }


def create_app() -> FastAPI:
    """Create and configure FastAPI application."""
    return app


def run_server(host: str = "0.0.0.0", port: int = 8000, reload: bool = False):
    """Run the FastAPI server."""
    logger.info(f"Starting server on {host}:{port}")
    
    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=reload,
        log_config=None  # Use our custom logging configuration
    )


if __name__ == "__main__":
    # Run with default settings
    run_server()
