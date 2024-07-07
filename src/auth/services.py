from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.auth.models import User
from src.auth.schemas import User as ValidUser
from src.database import get_db
from src.exceptions import CustomHTTPException

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(user: ValidUser, db: Session = Depends(get_db)):
    try:
        db_user = User(username=user.username, password=pwd_context.hash(user.password))
        db.add(db_user)
        db.commit()
    except IntegrityError:
        db.rollback()
        raise CustomHTTPException(status_code=400, reason="User has been registered.")
    except Exception as e:
        db.rollback()
        raise CustomHTTPException(status_code=500, reason=f"Internal Server Error: {str(e)}")
