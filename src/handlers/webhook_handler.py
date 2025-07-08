"""
Webhook handler for processing GitHub webhook events.
Handles signature verification, payload parsing, and sync coordination.
"""

import hmac
import hashlib
import json
from datetime import datetime
from typing import Dict, Any, Optional
from fastapi import Request, HTTPException
import asyncio

from ..config import get_config
from ..utils.logger import get_logger
from ..models.webhook_models import (
    WebhookEvent, WebhookParser, WebhookValidationError, 
    WebhookSignatureError, WebhookEventType
)
from ..services.sync_service import SyncService

logger = get_logger(__name__)


class WebhookHandler:
    """Handler for GitHub webhook events."""
    
    def __init__(self):
        """Initialize webhook handler."""
        self.config = get_config()
        self.settings = self.config.settings
        self.sync_service = SyncService()
        
        # Track webhook statistics
        self.webhook_stats = {
            "total_received": 0,
            "total_processed": 0,
            "total_failed": 0,
            "signature_failures": 0,
            "last_webhook_time": None
        }
    
    def verify_signature(self, signature: str, body: bytes) -> bool:
        """Verify GitHub webhook signature.
        
        Args:
            signature: X-Hub-Signature-256 header value
            body: Raw request body
            
        Returns:
            True if signature is valid, False otherwise
        """
        if not signature:
            logger.warning("No signature provided in webhook request")
            return False
        
        # Remove 'sha256=' prefix if present
        if signature.startswith('sha256='):
            signature = signature[7:]
        
        # Calculate expected signature
        expected_signature = hmac.new(
            self.settings.webhook_secret.encode('utf-8'),
            body,
            hashlib.sha256
        ).hexdigest()
        
        # Compare signatures using constant-time comparison
        is_valid = hmac.compare_digest(expected_signature, signature)
        
        if not is_valid:
            logger.warning("Invalid webhook signature", extra={
                "provided_signature": signature[:16] + "...",  # Log only first 16 chars for security
                "expected_signature": expected_signature[:16] + "..."
            })
            self.webhook_stats["signature_failures"] += 1
        
        return is_valid
    
    async def handle_webhook(self, request: Request) -> Dict[str, Any]:
        """Handle incoming webhook request.
        
        Args:
            request: FastAPI request object
            
        Returns:
            Dictionary with processing results
            
        Raises:
            HTTPException: If request is invalid
        """
        start_time = datetime.utcnow()
        self.webhook_stats["total_received"] += 1
        
        result = {
            "success": False,
            "event_type": None,
            "delivery_id": None,
            "action": None,
            "item_id": None,
            "error": None,
            "processing_time_ms": 0
        }
        
        try:
            # Get headers
            event_type = request.headers.get("X-GitHub-Event")
            delivery_id = request.headers.get("X-GitHub-Delivery")
            signature = request.headers.get("X-Hub-Signature-256")
            
            if not event_type:
                raise HTTPException(status_code=400, detail="Missing X-GitHub-Event header")
            
            if not delivery_id:
                raise HTTPException(status_code=400, detail="Missing X-GitHub-Delivery header")
            
            # Read request body
            body = await request.body()
            
            # Verify signature
            if not self.verify_signature(signature, body):
                raise WebhookSignatureError("Invalid webhook signature")
            
            # Parse JSON payload
            try:
                payload = json.loads(body.decode('utf-8'))
            except json.JSONDecodeError as e:
                raise WebhookValidationError(f"Invalid JSON payload: {e}")
            
            # Log webhook receipt
            from ..utils.logger import get_logger_manager
            logger_manager = get_logger_manager()
            logger_manager.log_webhook_event(
                logger, event_type, 
                payload.get('action', 'unknown'),
                delivery_id,
                payload.get('repository', {}).get('full_name')
            )
            
            # Update result with basic info
            result["event_type"] = event_type
            result["delivery_id"] = delivery_id
            result["action"] = payload.get('action')
            
            # Check if this event type should be processed
            if not self._should_process_event(event_type, payload.get('action')):
                logger.info(f"Ignoring webhook event {event_type}:{payload.get('action')}")
                result["success"] = True
                result["action"] = "ignored"
                return result
            
            # Create webhook event object
            webhook_event = WebhookParser.create_webhook_event(
                event_type, delivery_id, signature, payload
            )
            
            # Process the webhook event
            sync_result = await self.sync_service.sync_webhook_event(webhook_event)
            
            # Update result with sync outcome
            result.update(sync_result)
            result["item_id"] = webhook_event.get_item_id()
            
            if result["success"]:
                self.webhook_stats["total_processed"] += 1
            else:
                self.webhook_stats["total_failed"] += 1
                
        except WebhookSignatureError as e:
            logger.error(f"Webhook signature verification failed: {e}")
            result["error"] = "Invalid signature"
            self.webhook_stats["total_failed"] += 1
            raise HTTPException(status_code=401, detail="Invalid signature")
            
        except WebhookValidationError as e:
            logger.error(f"Webhook validation failed: {e}")
            result["error"] = str(e)
            self.webhook_stats["total_failed"] += 1
            raise HTTPException(status_code=400, detail=str(e))
            
        except Exception as e:
            logger.error(f"Unexpected error processing webhook: {e}")
            result["error"] = str(e)
            self.webhook_stats["total_failed"] += 1
            raise HTTPException(status_code=500, detail="Internal server error")
            
        finally:
            # Calculate processing time
            end_time = datetime.utcnow()
            processing_time = (end_time - start_time).total_seconds() * 1000
            result["processing_time_ms"] = round(processing_time, 2)
            
            # Update last webhook time
            self.webhook_stats["last_webhook_time"] = start_time
            
            # Log processing result
            logger.info("Webhook processing completed", extra={
                "delivery_id": result["delivery_id"],
                "event_type": result["event_type"],
                "action": result["action"],
                "success": result["success"],
                "processing_time_ms": result["processing_time_ms"]
            })
        
        return result
    
    def _should_process_event(self, event_type: str, action: Optional[str]) -> bool:
        """Check if a webhook event should be processed.
        
        Args:
            event_type: GitHub event type
            action: GitHub event action
            
        Returns:
            True if event should be processed
        """
        # Check against configuration
        return self.config.is_webhook_event_enabled(event_type, action or "")
    
    async def handle_ping(self, request: Request) -> Dict[str, Any]:
        """Handle GitHub webhook ping event.
        
        Args:
            request: FastAPI request object
            
        Returns:
            Dictionary with ping response
        """
        logger.info("Received GitHub webhook ping")
        
        body = await request.body()
        signature = request.headers.get("X-Hub-Signature-256")
        
        # Verify signature for ping as well
        if not self.verify_signature(signature, body):
            raise HTTPException(status_code=401, detail="Invalid signature")
        
        try:
            payload = json.loads(body.decode('utf-8'))
            zen = payload.get('zen', 'GitHub webhook ping received')
            
            return {
                "success": True,
                "message": "Webhook endpoint is active",
                "zen": zen,
                "timestamp": datetime.utcnow().isoformat()
            }
            
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid JSON payload")
    
    def get_webhook_stats(self) -> Dict[str, Any]:
        """Get webhook processing statistics.
        
        Returns:
            Dictionary with webhook statistics
        """
        stats = self.webhook_stats.copy()
        
        # Add calculated fields
        if stats["total_received"] > 0:
            stats["success_rate"] = (stats["total_processed"] / stats["total_received"]) * 100
            stats["failure_rate"] = (stats["total_failed"] / stats["total_received"]) * 100
        else:
            stats["success_rate"] = 0.0
            stats["failure_rate"] = 0.0
        
        return stats
    
    async def validate_webhook_config(self) -> Dict[str, Any]:
        """Validate webhook configuration.
        
        Returns:
            Dictionary with validation results
        """
        validation_result = {
            "success": False,
            "webhook_secret_configured": False,
            "sync_service_ready": False,
            "enabled_events": [],
            "errors": []
        }
        
        try:
            # Check webhook secret
            if self.settings.webhook_secret:
                validation_result["webhook_secret_configured"] = True
            else:
                validation_result["errors"].append("Webhook secret not configured")
            
            # Check sync service
            sync_validation = await self.sync_service.validate_sync_setup()
            validation_result["sync_service_ready"] = sync_validation["success"]
            if not sync_validation["success"]:
                validation_result["errors"].extend(sync_validation["errors"])
            
            # Get enabled events
            validation_result["enabled_events"] = list(self.config.webhook_events.keys())
            
            # Overall success
            validation_result["success"] = (
                validation_result["webhook_secret_configured"] and
                validation_result["sync_service_ready"]
            )
            
        except Exception as e:
            validation_result["errors"].append(f"Webhook validation error: {e}")
        
        return validation_result
    
    async def process_test_webhook(self, event_type: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Process a test webhook event (for testing purposes).
        
        Args:
            event_type: GitHub event type
            payload: Webhook payload
            
        Returns:
            Dictionary with processing results
        """
        try:
            # Create a test webhook event
            webhook_event = WebhookParser.create_webhook_event(
                event_type,
                "test-delivery-id",
                "test-signature",
                payload
            )
            
            # Process the event
            result = await self.sync_service.sync_webhook_event(webhook_event)
            
            logger.info("Test webhook processed", extra={
                "event_type": event_type,
                "action": payload.get('action'),
                "success": result["success"]
            })
            
            return result
            
        except Exception as e:
            logger.error(f"Error processing test webhook: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def reset_stats(self):
        """Reset webhook statistics."""
        self.webhook_stats = {
            "total_received": 0,
            "total_processed": 0,
            "total_failed": 0,
            "signature_failures": 0,
            "last_webhook_time": None
        }
        logger.info("Webhook statistics reset")


class WebhookMiddleware:
    """Middleware for webhook request processing."""
    
    def __init__(self, handler: WebhookHandler):
        """Initialize middleware.
        
        Args:
            handler: Webhook handler instance
        """
        self.handler = handler
    
    async def __call__(self, request: Request, call_next):
        """Process webhook request with middleware.
        
        Args:
            request: FastAPI request object
            call_next: Next middleware/endpoint
            
        Returns:
            Response
        """
        # Add request ID for tracking
        import uuid
        request_id = str(uuid.uuid4())[:8]
        
        # Add to request state
        request.state.request_id = request_id
        
        # Log request start
        logger.debug(f"Webhook request started", extra={
            "request_id": request_id,
            "method": request.method,
            "url": str(request.url),
            "headers": dict(request.headers)
        })
        
        # Process request
        response = await call_next(request)
        
        # Log request completion
        logger.debug(f"Webhook request completed", extra={
            "request_id": request_id,
            "status_code": response.status_code
        })
        
        return response


def create_webhook_handler() -> WebhookHandler:
    """Create and configure webhook handler.
    
    Returns:
        Configured WebhookHandler instance
    """
    handler = WebhookHandler()
    
    # Log handler creation
    logger.info("Webhook handler created", extra={
        "enabled_events": list(handler.config.webhook_events.keys())
    })
    
    return handler
