from datetime import date

from pydantic import BaseModel, EmailStr


class TeacherCreateRequest(BaseModel):
    # Account
    email: EmailStr
    password: str

    # Person
    first_name: str
    last_name: str
    date_of_birth: date | None = None
    gender: str | None = None
    phone: str | None = None
    address: str | None = None

    # Teacher
    employee_number: str
    designation: str | None = None
    hire_date: date | None = None
    status: str = "active"


class TeacherProfileResponse(BaseModel):
    id: int
    employee_number: str
    designation: str | None
    hire_date: date | None
    status: str

    model_config = {
        "from_attributes": True
    }


class TeacherMeResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    first_name: str
    last_name: str
    date_of_birth: date | None
    gender: str | None
    phone: str | None
    address: str | None

    teacher_profile: TeacherProfileResponse