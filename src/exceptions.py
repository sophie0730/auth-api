from fastapi import HTTPException


class CustomHTTPException(HTTPException):
    def __init__(self, status_code: int, reason: str):
        super().__init__(status_code=status_code, detail={"success": False, "reason": reason})
