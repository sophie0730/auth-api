from fastapi.exceptions import RequestValidationError


def parse_validation_exception(exc: RequestValidationError) -> str:
    if isinstance(exc.errors(), str):
        return exc.errors()

    error = exc.errors()[0]
    location = "Unknown" if len(error["loc"]) < 1 else error["loc"][1]

    if location == "Unknown":
        return "There is an unknown issue about request validation error."

    return f"Ensure the length of {location} should be in a property range"  # noqa: E501
