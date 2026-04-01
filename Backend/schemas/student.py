from pydantic import BaseModel, EmailStr, ConfigDict, field_validator
from enum import Enum
from datetime import date
from decimal import Decimal

class AcademicYear(str, Enum):
    freshman= "freshman"
    sophomore= "sophomore"
    junior= "junior"
    senior_1= "senior_1"
    senior_2= "senior_2"

class StudentBase(BaseModel):
    full_name: str
    national_id: str
    phone: str
    birth_date: date
    address: str | None=None
    enroll_date: date
    expected_graduation: date | None=None
    academic_year: AcademicYear
    current_gpa: Decimal = Decimal("0.00")

    @field_validator("current_gpa")
    def validate_gpa(cls, v):
        if v < 0 or v > 4:
            raise ValueError("GPA must be between 0 and 4")
        return v

    @field_validator("national_id")
    def validate_national_id(cls, v):
        if len(v) != 14 or not v.isdigit():
            raise ValueError("National ID must be 14 digits")
        return v

    model_config = ConfigDict(extra="forbid")

class StudentCreate(StudentBase):
    university_id: str

    model_config = ConfigDict(extra="forbid")


class StudentAdminUpdate(BaseModel):
    full_name: str | None = None
    phone: str | None = None
    address: str | None = None
    enroll_date: date | None = None
    academic_year: AcademicYear | None = None
    expected_graduation: date | None = None
    current_gpa: Decimal | None = None

    model_config = ConfigDict(extra="forbid")


class StudentDetailedResponse(StudentBase):
    user_id: int
    university_id: str
    email: EmailStr | None=None

    model_config = ConfigDict(from_attributes=True)   


class StudentResponse(StudentBase):
    user_id: int
    university_id: str
    passed_credits: int | None=None
    registered_credits: int | None=None

    model_config = ConfigDict(from_attributes=True)


class StudentListResponse(BaseModel):
    user_id: int
    university_id: str
    full_name: str
    academic_year: AcademicYear
    current_gpa: Decimal

    model_config = ConfigDict(from_attributes=True)
