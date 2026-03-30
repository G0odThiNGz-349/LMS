from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, Field
from enum import Enum
from datetime import date
from decimal import Decimal


class UserRole(str, Enum):
    student = "student"
    professor = "professor"
    teaching_assistant = "teaching_assistant"

class AcademicYear(str, Enum):
    freshman= "freshman"
    sophomore= "sophomore"
    junior= "junior"
    senior_1= "senior_1"
    senior_2= "senior_2"

class CreateUserStudent(BaseModel):
    university_id: str
    email: EmailStr | None=None
    role: UserRole
    is_active: bool = True
    password:str = Field(min_length=8, max_length=128)
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


class CreateUserProfessor(BaseModel):
    university_id: str
    email: EmailStr | None=None
    role: UserRole
    is_active: bool = True
    password:str = Field(min_length=8, max_length=128)
    full_name: str
    address: str | None=None
    department_id: str
    hire_date: date

    model_config = ConfigDict(extra="forbid")