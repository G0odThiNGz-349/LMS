from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from Backend.database import get_db                    
from Backend.auth.dep import get_current_user      
from Backend.models import User
import Backend.crud.examResults as examResultsCrud
import Backend.schemas.examResults as examResultsSchema
 
router = APIRouter()

result_router = APIRouter(prefix="/exam-results", tags=["Exam Results"])
 
 
@result_router.get("/exam/{exam_id}", response_model=list[examResultsSchema.ExamResultOut])
def list_results_for_exam(exam_id: int, db: Session = Depends(get_db)):
    return examResultsCrud.get_results_for_exam(db, exam_id)
 
 
@result_router.get("/{result_id}", response_model=examResultsSchema.ExamResultOut)
def get_result(result_id: int, db: Session = Depends(get_db)):
    return examResultsCrud.get_result(db, result_id)
 
 
@result_router.post("/", response_model=examResultsSchema.ExamResultOut, status_code=status.HTTP_201_CREATED)
def create_result(data: examResultsSchema.ExamResultCreate, db: Session = Depends(get_db)):
    return examResultsCrud.create_result(db, data)
 
 
@result_router.patch("/{result_id}", response_model=examResultsSchema.ExamResultOut)
def update_result(
    result_id: int,
    data: examResultsSchema.ExamResultUpdate,
    db: Session = Depends(get_db),
):
    return examResultsCrud.update_result(db, result_id, data)
 
 
@result_router.delete("/{result_id}")
def delete_result(result_id: int, db: Session = Depends(get_db)):
    return examResultsCrud.delete_result(db, result_id)



my_result_router = APIRouter(prefix="/me/exam-results", tags=["My Exam Results"])
 
 
@my_result_router.get("/", response_model=list[examResultsSchema.MyExamResultOut])
def my_exam_results(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return examResultsCrud.get_my_exam_results(db, current_user_id=current_user.id)
 
 
@my_result_router.get("/{exam_id}", response_model=examResultsSchema.MyExamResultOut)
def my_result_for_exam(
    exam_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return examResultsCrud.get_my_result_for_exam(db, exam_id, current_user_id=current_user.id)