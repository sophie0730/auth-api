from fastapi.exceptions import RequestValidationError


def parse_validation_exception(exc: RequestValidationError) -> str:
    if isinstance(exc.errors(), str):
        return exc.errors()

    error = exc.errors()[0]
    location = "Unknown" if len(error["loc"]) < 1 else error["loc"][1]
    msg = error["msg"]

    return f"{location} : {msg}"
