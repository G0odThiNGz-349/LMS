from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal
from datetime import datetime
from enum import Enum

class EnrollmentStatus(str, Enum):
    active = "active"
    passed = "passed"
    failed = "failed"
    dropped = "dropped"


class EnrollmentCreate(BaseModel):
    student_user_id: int
    course_offering_id: int
    status: EnrollmentStatus = Field(default=EnrollmentStatus.active)

    model_config = ConfigDict(extra="forbid")


class EnrollmentUpdate(BaseModel):
    student_user_id: int | None=None
    course_offering_id: int | None=None
    status: EnrollmentStatus | None=None
    enrolled_at: datetime | None=None
    grade: Decimal | None=None

    model_config = ConfigDict(extra="forbid")


class EnrollmentResponse(BaseModel):
    course_offering_id: int
    course_name: str
    course_code: str
    semester_name: str
    status: EnrollmentStatus
    enrolled_at: datetime
    grade: Decimal | None=None

    model_config = ConfigDict(from_attributes=True)