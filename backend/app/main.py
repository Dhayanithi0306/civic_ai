import time
import uuid
import logging
import contextvars
# pyrefly: ignore [missing-import]
from fastapi import FastAPI, Request, HTTPException
# pyrefly: ignore [missing-import]
from fastapi.responses import JSONResponse
# pyrefly: ignore [missing-import]
from fastapi.middleware.cors import CORSMiddleware
from app.routes import chat, complaints, recommend
from app.utils.json_loader import JSONLoader
from app.config import config
from app.services.complaint_service import ComplaintService

# Context variable for request ID tracking
request_id_var = contextvars.ContextVar("request_id", default="SYSTEM")

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [ReqID: %(request_id)s] %(name)s: %(message)s"
)

# Robustly inject request_id into every log record
old_factory = logging.getLogRecordFactory()

def record_factory(*args, **kwargs):
    record = old_factory(*args, **kwargs)
    record.request_id = request_id_var.get()
    return record

logging.setLogRecordFactory(record_factory)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="CivicAI API",
    description="Backend API for GenAI-powered civic platform. Standardized responses and robust AI.",
    version="1.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def request_tracking_middleware(request: Request, call_next):
    """Middleware for structured request tracking and timing."""
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    request_id_var.set(request_id)
    
    start_time = time.time()
    
    logging.info(f"REQUEST START: {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    
    logging.info(f"REQUEST END: {request.method} {request.url.path} - Status: {response.status_code} - Time: {process_time:.4f}s")
    return response

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Standardized HTTP Exception response."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"success": False, "message": exc.detail, "error": f"HTTP_{exc.status_code}"},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Standardized unhandled exception response."""
    logging.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"success": False, "message": "An internal server error occurred.", "error": str(exc)},
    )

@app.on_event("startup")
async def startup_event():
    """Initialize application state."""
    logger.info("Initializing CivicAI...")
    JSONLoader.load_schemes()
    ComplaintService.load_complaints()

app.include_router(chat.router, prefix="/chat", tags=["Chat"])
app.include_router(complaints.router, prefix="/complaints", tags=["Complaints"])
app.include_router(recommend.router, prefix="/recommend", tags=["Recommend"])

@app.get("/health")
def health_check():
    """Health check endpoint to verify system status."""
    return {
        "status": "healthy",
        "gemini": "connected" if config.GEMINI_API_KEY else "disconnected",
        "schemes_loaded": len(JSONLoader.load_schemes()),
        "complaints_loaded": len(ComplaintService.get_all_complaints())
    }
