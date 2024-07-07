import re

from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, field_validator


class User(BaseModel):
    username: str = Field(..., max_length=32, min_length=3)
    password: str = Field(..., max_length=32, min_length=8)

    @field_validator("password")
    def password_validate(cls, v: str) -> str:
        if not re.search(r"(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])", v):
            raise RequestValidationError(
                "Password must contain at least 1 uppercase letter, 1 lowercase letter and at least 1 number"  # noqa: E501
            )

        return v


class ResponseModel(BaseModel):
    success: bool
    reason: str
