from datetime import date

from pydantic import BaseModel, EmailStr


class StudentProfileResponse(BaseModel):
    id: int
    student_number: str
    admission_date: date | None
    status: str

    model_config = {
        "from_attributes": True
    }


class StudentMeResponse(BaseModel):
    id: int
    email: EmailStr
    is_active: bool

    first_name: str
    last_name: str
    date_of_birth: date | None
    gender: str | None
    phone: str | None
    address: str | None

    student_profile: StudentProfileResponse

from datetime import date

from pydantic import BaseModel, EmailStr


class StudentCreateRequest(BaseModel):
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

    # Student
    student_number: str
    admission_date: date | None = None
    status: str = "active"