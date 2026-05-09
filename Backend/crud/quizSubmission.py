from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from Backend.models import QuizSubmission
from Backend.schemas.quizSubmission import QuizSubmissionCreate, QuizSubmissionUpdate



def get_submission(db: Session, submission_id: int):
    sub = db.query(QuizSubmission).filter(QuizSubmission.id == submission_id).first()
    if not sub:
        raise HTTPException(status_code=404, detail="Submission not found")
    return sub
 
 
def get_submissions_for_quiz(db: Session, quiz_id: int):
    return db.query(QuizSubmission).filter(QuizSubmission.quiz_id == quiz_id).all()
 
 
def create_submission(db: Session, data: QuizSubmissionCreate):
    sub = QuizSubmission(**data.model_dump())
    db.add(sub)
    db.commit()
    db.refresh(sub)
    return sub
 
 
def update_submission(db: Session, submission_id: int, data: QuizSubmissionUpdate):
    sub = get_submission(db, submission_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(sub, field, value)
    db.commit()
    db.refresh(sub)
    return sub
 
 
def delete_submission(db: Session, submission_id: int):
    sub = get_submission(db, submission_id)
    db.delete(sub)
    db.commit()
    return {"detail": "Submission deleted"}
 
 
def get_my_quiz_submissions(db: Session, current_user_id: int):
    return (
        db.query(QuizSubmission)
        .filter(QuizSubmission.student_user_id == current_user_id)
        .all()
    )