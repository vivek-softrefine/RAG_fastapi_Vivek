from typing import Any

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    """Common schema for API error responses."""

    status: str = "error"
    message: str
    details: list[dict[str, Any]] | None = None