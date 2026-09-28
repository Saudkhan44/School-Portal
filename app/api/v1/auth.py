from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.exceptions import AppException
from app.db.session import get_db
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.auth import login_user


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post(
    "/login",
    response_model=TokenResponse,
)
def login(
    data: LoginRequest,
    db: Session = Depends(get_db),
):
    try:
        token = login_user(
            db=db,
            email=data.email,
            password=data.password,
        )

        return {
            "access_token": token,
            "token_type": "bearer",
        }

    except AppException as exc:
        raise exc