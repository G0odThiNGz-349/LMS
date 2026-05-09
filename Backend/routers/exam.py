from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from Backend.database import get_db                    
from Backend.auth.dep import get_current_user      
from Backend.models import User
import Backend.crud.exam as examCrud
import Backend.schemas.exam as examSchema
 
router = APIRouter()

exam_router = APIRouter(prefix="/exams", tags=["Exams"])
 
@exam_router.get("/", response_model=list[examSchema.ExamOut])
def list_exams(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return examCrud.get_exams(db, skip=skip, limit=limit)
 
 
@exam_router.get("/{exam_id}", response_model=examSchema.ExamOut)
def get_exam(exam_id: int, db: Session = Depends(get_db)):
    return examCrud.get_exam(db, exam_id)
 
 
@exam_router.post("/", response_model=examSchema.ExamOut, status_code=status.HTTP_201_CREATED)
def create_exam(data: examSchema.ExamCreate, db: Session = Depends(get_db)):
    return examCrud.create_exam(db, data)
 
 
@exam_router.patch("/{exam_id}", response_model=examSchema.ExamOut)
def update_exam(exam_id: int, data: examSchema.ExamUpdate, db: Session = Depends(get_db)):
    return examCrud.update_exam(db, exam_id, data)
 
 
@exam_router.delete("/{exam_id}")
def delete_exam(exam_id: int, db: Session = Depends(get_db)):
    return examCrud.delete_exam(db, exam_id)