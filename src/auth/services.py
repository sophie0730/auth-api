from fastapi import Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.auth.dependencies import get_db
from src.auth.hashing import hash_password, verify_password
from src.auth.models import User
from src.auth.rate_limiter import check_lockout, record_failed_attempt, reset_failed_attemps
from src.auth.schemas import User as ValidUser
from src.exceptions import CustomHTTPException
from src.log import logger


def get_user(username: str, db: Session = Depends(get_db)):
    return db.query(User).filter(User.username == username).first()


def create_user(user: ValidUser, db: Session = Depends(get_db)):
    try:
        db_user = User(username=user.username, password=hash_password(user.password))
        db.add(db_user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise CustomHTTPException(status_code=400, reason="User has been registered.")
    except Exception as e:
        db.rollback()
        raise CustomHTTPException(status_code=500, reason=f"Internal Server Error: {str(e)}")


async def verify_user(username: str, password: str, db: Session = Depends(get_db)):
    try:
        if await check_lockout(username):
            logger.warning(f"User {username} is locked out due to too many failed login attempts.")
            raise CustomHTTPException(
                status_code=429,
                reason="You have failed to login five times, please wait one minute to login again",
            )

        current_user = get_user(username, db)

        if not current_user:
            await handled_failed_attempt(username, "The username doesn't exist", 404)
        if not verify_password(password, current_user.password):
            await handled_failed_attempt(username, "The password is wrong", 400)

        await reset_failed_attemps(username)

    except CustomHTTPException as e:
        raise e
    except Exception as e:
        raise CustomHTTPException(status_code=500, reason=f"Internal Server Error: {str(e)}")


async def handled_failed_attempt(username: str, reason: str, status_code: int):
    await record_failed_attempt(username)
    raise CustomHTTPException(status_code=status_code, reason=reason)
