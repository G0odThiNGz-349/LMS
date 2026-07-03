from typing import Optional
from pydantic import BaseModel, ConfigDict
from decimal import Decimal


class ExamResultBase(BaseModel):
    exam_id: int
    student_user_id: int
    score: Optional[Decimal] = None
    percentage: Optional[Decimal] = None
 
 
class ExamResultCreate(ExamResultBase):
    pass

    model_config = ConfigDict(extra="forbid")
 
 
class ExamResultUpdate(BaseModel):
    score: Optional[Decimal] = None
    percentage: Optional[Decimal] = None

    model_config = ConfigDict(extra="forbid")
 
 
class ExamResultOut(ExamResultBase):
    id: int
 
    class Config:
        from_attributes = True
 
 
class MyExamResultOut(BaseModel):
    exam_id: int
    score: Optional[Decimal]
    percentage: Optional[Decimal]
    subject: str          
    term: str             
    credits: int          
    grade: Optional[str]
    exam_type: str 

    class Config:
        from_attributes = True