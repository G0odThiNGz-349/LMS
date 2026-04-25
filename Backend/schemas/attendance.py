from pydantic import BaseModel, ConfigDict
from datetime import datetime, date
from enum import Enum

class AttendanceStatus(str, Enum):
    present = "present"
    absent = "absent"
    late = "late"
    excused = "excused"

class AttendanceCreate(BaseModel):
    status: AttendanceStatus

    model_config = ConfigDict(extra="forbid")


class AttendanceUpdate(BaseModel):
    course_offering_id: int | None=None
    session_date: date | None=None
    status: AttendanceStatus | None=None

    model_config = ConfigDict(extra="forbid")


class AttendanceResponse(BaseModel):
    student_name: str
    course_name: str
    course_code: str
    session_date: date
    status: AttendanceStatus 
    recorded_at: datetime

    model_config= ConfigDict(from_attributes=True)