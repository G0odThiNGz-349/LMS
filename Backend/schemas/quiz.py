from datetime import date, datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict 
from Backend.models import QuizType  
 
 
class QuizBase(BaseModel):
    course_offering_id: int
    quiz_type: QuizType
    title: str
    description: Optional[str] = None
    scheduled_date: date
    duration_min: int = 30
    total_marks: int = 10
 
 
class QuizCreate(QuizBase):
    pass

    model_config = ConfigDict(extra="forbid")
 
 
class QuizUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_date: Optional[date] = None
    duration_min: Optional[int] = None
    total_marks: Optional[int] = None

    model_config = ConfigDict(extra="forbid")
 
 
class QuizOut(QuizBase):
    id: int
    created_at: datetime
 
    class Config:
        from_attributes = True