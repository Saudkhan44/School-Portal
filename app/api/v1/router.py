from fastapi import APIRouter

from app.api.v1 import (
    admin,
    auth,
    students,
    teachers,
    users,
)
from app.core.config import settings


router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "environment": settings.environment,
    }


router.include_router(auth.router)
router.include_router(users.router)
router.include_router(students.router)
router.include_router(teachers.router)
router.include_router(admin.router)