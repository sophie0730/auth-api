from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from src.auth.router import router as auth_router
from src.database import Base, engine
from src.exceptions import CustomHTTPException
from src.utils import parse_validation_exception

app = FastAPI()

Base.metadata.create_all(bind=engine)
app.include_router(auth_router, prefix="/api/v1", tags=["auth"])


@app.exception_handler(CustomHTTPException)
async def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    try:
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": exc.detail["success"], "reason": exc.detail["reason"]},
        )
    except Exception as e:
        raise CustomHTTPException(status_code=500, reason=f"Internal Server Error: {str(e)}")


@app.exception_handler(RequestValidationError)
async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
    try:
        res = parse_validation_exception(exc)
        return JSONResponse(status_code=422, content={"success": False, "reason": res})
    except Exception as e:
        raise CustomHTTPException(status_code=500, reason=f"Internal Server Error: {str(e)}")


@app.get("/")
def root():
    return {"msg": "HTTP RESTful API for account management"}
