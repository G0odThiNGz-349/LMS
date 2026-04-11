from pydantic import BaseModel, Field
from datetime import date, datetime
from decimal import Decimal
from typing import List, Generic, TypeVar

from Backend.models import (
    AttendanceStatus,
    EnrollmentStatus,
    AcademicYear
)


T = TypeVar("T")
class PaginatedResponse(BaseModel, Generic[T]):
    page: int
    page_size: int
    data: List[T]


class ExportStudent(BaseModel):
    user_id: int
    full_name: str
    birth_date: date
    enroll_date: date
    expected_graduation: date
    academic_year: AcademicYear
    current_gpa: Decimal | None = Field(default=0.00, ge=0, le=4.00)
    passed_credits: int = 0
    registered_credits: int = 0
    department : str | None=None

    class Config:
        from_attributes = True


class ExportAttendance(BaseModel):
    student_user_id: int
    course_offering_id: int
    session_date: date
    status: AttendanceStatus
    recorded_at: datetime

    class Config:
        from_attributes = True


class ExportEnrollment(BaseModel):
    student_user_id: int
    course_offering_id: int
    grade: Decimal | None = None
    status: EnrollmentStatus
    enrolled_at: datetime

    class Config:
        from_attributes = True


class ExportCourseOffering(BaseModel):
    id: int
    course_id: int
    semester_id: int
    professor_user_id: int
    start_date: date | None = None
    end_date: date | None = None

    class Config:
        from_attributes = True