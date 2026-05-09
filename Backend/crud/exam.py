from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from Backend.models import Exam
from Backend.schemas.exam import ExamCreate,ExamUpdate



def get_exam(db: Session, exam_id: int):
    exam = db.query(Exam).filter(Exam.id == exam_id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")
    return exam
 
 
def create_exam(db: Session, data: ExamCreate):
    exam = Exam(**data.model_dump())
    db.add(exam)
    db.commit()
    db.refresh(exam)
    return exam
 
 
def update_exam(db: Session, exam_id: int, data: ExamUpdate):
    exam = get_exam(db, exam_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(exam, field, value)
    db.commit()
    db.refresh(exam)
    return exam
 
 
def delete_exam(db: Session, exam_id: int):
    exam = get_exam(db, exam_id)
    db.delete(exam)
    db.commit()
    return {"detail": "Exam deleted"}