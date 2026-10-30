from fastapi import FastAPI

app = FastAPI(
    title="AI-Powered Personal Knowledge Assistant",
    description="An AI-powered assistant for personal documents and Google Workspace.",
    version="1.0.0",
)

@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "success",
        "message": "Application is running.",
    }