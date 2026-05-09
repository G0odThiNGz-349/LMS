from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from Backend.models import Quiz
from Backend.schemas.quiz import QuizCreate, QuizUpdate



def get_quiz(db: Session, quiz_id: int):
    quiz = db.query(Quiz).filter(Quiz.id == quiz_id).first()
    if not quiz:
        raise HTTPException(status_code=404, detail="Quiz not found")
    return quiz
 
 
def create_quiz(db: Session, data: QuizCreate):
    quiz = Quiz(**data.model_dump())
    db.add(quiz)
    db.commit()
    db.refresh(quiz)
    return quiz
 
 
def update_quiz(db: Session, quiz_id: int, data: QuizUpdate):
    quiz = get_quiz(db, quiz_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(quiz, field, value)
    db.commit()
    db.refresh(quiz)
    return quiz
 
 
def delete_quiz(db: Session, quiz_id: int):
    quiz = get_quiz(db, quiz_id)
    db.delete(quiz)
    db.commit()
    return {"detail": "Quiz deleted"}