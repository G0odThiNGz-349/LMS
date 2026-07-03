from datetime import date, datetime
from decimal import Decimal
from typing import Optional
from pydantic import BaseModel, ConfigDict



class QuizSubmissionBase(BaseModel):
    quiz_id: int
    student_user_id: int
    score: Optional[Decimal] = None
    percentage: Optional[Decimal] = None
    submitted_at: Optional[datetime] = None
 
 
class QuizSubmissionCreate(QuizSubmissionBase):
    pass

    model_config = ConfigDict(extra="forbid")
 
 
class QuizSubmissionUpdate(BaseModel):
    score: Optional[Decimal] = None
    percentage: Optional[Decimal] = None
    submitted_at: Optional[datetime] = None

    model_config = ConfigDict(extra="forbid")
 
 
class QuizSubmissionOut(BaseModel):
    quiz_id: int
    score: Optional[Decimal] = None
    percentage: Optional[Decimal] = None
    submitted_at: Optional[datetime] = None
    subject: str          
    term: str            
    credits: int          
    grade: Optional[str]
    quiz_type: str  
 
    class Config:
        from_attributes = True