from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=20_000)
    language: str | None = Field(default=None, pattern="^(ar|en)$")


class TaskCreate(BaseModel):
    title: str = Field(min_length=1, max_length=500)
    due_at: str | None = Field(default=None, max_length=80)


class NoteCreate(BaseModel):
    title: str = Field(min_length=1, max_length=300)
    content: str = Field(min_length=1, max_length=20_000)


class AssistantMessage(BaseModel):
    message: str = Field(min_length=1, max_length=2_000)


class HealthResponse(BaseModel):
    name: str
    version: str
    status: str
    model_ready: bool
