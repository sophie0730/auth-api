from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.auth.schemas import ResponseModel, User
from src.auth.services import create_user, verify_user
from src.database import get_db

router = APIRouter()


@router.post(
    "/signup",
    response_model=ResponseModel,
    status_code=201,
    responses={
        201: {
            "description": "User Account created successfully",
            "content": {
                "application/json": {
                    "example": {"success": True, "reason": "User created successfully"}
                }
            },
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "examples": {
                        "User has been registered": {
                            "value": {
                                "success": False,
                                "reason": "User has been registered.",
                            },
                        },
                    }
                },
            },
        },
        422: {
            "description": "Request Validation Error",
            "content": {
                "application/json": {
                    "examples": {
                        "Username has wrong Input length": {
                            "value": {
                                "success": False,
                                "reason": "username : String should have at least 3 characters",
                            },
                        },
                        "Password has wrong Input length": {
                            "value": {
                                "success": False,
                                "reason": "password : String should have at least 8 characters",
                            },
                        },
                        "The formatting of the password is wrong": {
                            "value": {
                                "success": False,
                                "reason": "Password must contained at least 1 uppercase letter, 1 lowercase letter, and 1 number.",  # noqa: E501
                            },
                        },
                    }
                },
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {"success": False, "reason": "Internal Server Error"}
                }
            },
        },
    },
)
def signup(user: User, db: Session = Depends(get_db)):
    create_user(user, db)
    return ResponseModel(success=True, reason="User created successfully")


@router.post(
    "/signin",
    response_model=ResponseModel,
    status_code=200,
    responses={
        200: {
            "description": "User sign in successfully",
            "content": {
                "application/json": {
                    "example": {"success": True, "reason": "User sign in successfully"}
                }
            },
        },
        400: {
            "description": "Bad Request",
            "content": {
                "application/json": {
                    "examples": {
                        "Password is not correct": {
                            "value": {
                                "success": False,
                                "reason": "Password is not correct",
                            },
                        },
                    }
                },
            },
        },
        422: {
            "description": "Request Validation Error",
            "content": {
                "application/json": {
                    "examples": {
                        "Username has wrong Input length": {
                            "value": {
                                "success": False,
                                "reason": "username : String should have at least 3 characters",
                            },
                        },
                        "Password has wrong Input length": {
                            "value": {
                                "success": False,
                                "reason": "password : String should have at least 8 characters",
                            },
                        },
                        "The formatting of the password is wrong": {
                            "value": {
                                "success": False,
                                "reason": "Password must contained at least 1 uppercase letter, 1 lowercase letter, and 1 number.",  # noqa: E501
                            },
                        },
                    }
                },
            },
        },
        429: {
            "description": "To Many Request",
            "content": {
                "application/json": {
                    "example": {
                        "success": False,
                        "reason": "You have failed to login five times, please wait one minute to login again",  # noqa: E501
                    }
                }
            },
        },
        500: {
            "description": "Internal Server Error",
            "content": {
                "application/json": {
                    "example": {"success": False, "reason": "Internal Server Error"}
                }
            },
        },
    },
)
def signin(user: User, db: Session = Depends(get_db)):
    verify_user(user.username, user.password, db)
    return ResponseModel(success=True, reason="User sign in successfully")
