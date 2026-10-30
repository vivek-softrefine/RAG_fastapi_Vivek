from fastapi import FastAPI
from dotenv import load_dotenv

from app.utils.error_handlers import ErrorHandlers
from app.utils.log_utils import LogUtils

load_dotenv()
LogUtils.configure_logging()

logger = LogUtils.get_logger(__name__)

app = FastAPI(
    title="AI-Powered Personal Knowledge Assistant",
    description="An AI-powered assistant for personal documents and Google Workspace.",
    version="1.0.0",
)

ErrorHandlers.register_handlers(app)

@app.get("/health")
async def health():
    logger.info("Health check endpoint called. Server is Healthy.")

    return {
        "status": "success",
        "message": "Application is running.",
    }