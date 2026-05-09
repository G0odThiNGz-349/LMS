from datetime import date
from typing import Optional
from pydantic import BaseModel, ConfigDict
from Backend.models import ExamsType


class ExamBase(BaseModel):
    course_offering_id: int
    exam_type: Optional[ExamsType] = None
    exam_date: date
    duration_min: int = 90
    total_marks: int = 30
    room: Optional[str] = None
 
 
class ExamCreate(ExamBase):
    pass

    model_config = ConfigDict(extra="forbid")
 
 
class ExamUpdate(BaseModel):
    exam_type: Optional[ExamsType] = None
    exam_date: Optional[date] = None
    duration_min: Optional[int] = None
    total_marks: Optional[int] = None
    room: Optional[str] = None
 
 
class ExamOut(ExamBase):
    id: int
 
    class Config:
        from_attributes = True