from fastapi import Depends, FastAPI
from fastapi.responses import JSONResponse

from .config import settings
from .schemas import ChatRequest, HealthResponse
from .security import require_admin_token

app = FastAPI(title=settings.app_name, version=settings.version)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(
        name=settings.app_name,
        version=settings.version,
        status="online",
        model_ready=False,
    )


@app.get("/api/v1/status", dependencies=[Depends(require_admin_token)])
async def status():
    return {
        "core": "online",
        "model": "not_initialized",
        "training": "idle",
        "memory": "not_configured",
        "internet_research": "not_configured",
    }


@app.post("/api/v1/chat", dependencies=[Depends(require_admin_token)])
async def chat(payload: ChatRequest):
    # Deliberately honest: there are no pretrained weights and no trained model yet.
    return JSONResponse(
        status_code=503,
        content={
            "status": "model_not_ready",
            "message": "MOHSEN has no trained language model yet.",
            "detail": "The model will be implemented and trained in a later milestone.",
        },
    )
