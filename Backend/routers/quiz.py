from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from Backend.database import get_db                    
from Backend.auth.dep import get_current_user      
from Backend.models import User
import Backend.crud.quiz as quizCrud
import Backend.schemas.quiz as quizSchema
 
router = APIRouter()


quiz_router = APIRouter(prefix="/quizzes", tags=["Quizzes"])
 
 
@quiz_router.get("/", response_model=list[quizSchema.QuizOut])
def list_quizzes(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    return quizCrud.get_quizzes(db, skip=skip, limit=limit)
 
 
@quiz_router.get("/{quiz_id}", response_model=quizSchema.QuizOut)
def get_quiz(quiz_id: int, db: Session = Depends(get_db)):
    return quizCrud.get_quiz(db, quiz_id)
 
 
@quiz_router.post("/", response_model=quizSchema.QuizOut, status_code=status.HTTP_201_CREATED)
def create_quiz(data: quizSchema.QuizCreate, db: Session = Depends(get_db)):
    return quizCrud.create_quiz(db, data)
 
 
@quiz_router.patch("/{quiz_id}", response_model=quizSchema.QuizOut)
def update_quiz(quiz_id: int, data: quizSchema.QuizUpdate, db: Session = Depends(get_db)):
    return quizCrud.update_quiz(db, quiz_id, data)
 
 
@quiz_router.delete("/{quiz_id}")
def delete_quiz(quiz_id: int, db: Session = Depends(get_db)):
    return quizCrud.delete_quiz(db, quiz_id)