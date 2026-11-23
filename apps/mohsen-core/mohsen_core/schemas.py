from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=20_000)
    language: str | None = Field(default=None, pattern="^(ar|en)$")


class ChatResponse(BaseModel):
    status: str
    message: str
    detail: str


class HealthResponse(BaseModel):
    name: str
    version: str
    status: str
    model_ready: bool
