from sqlalchemy.orm import Session
from fastapi import HTTPException
from Backend.models import ExamResult
from Backend.schemas.examResults import ExamResultCreate, ExamResultUpdate



def get_result(db: Session, result_id: int):
    result = db.query(ExamResult).filter(ExamResult.id == result_id).first()
    if not result:
        raise HTTPException(status_code=404, detail="Exam result not found")
    return result
 
 
def get_results_for_exam(db: Session, exam_id: int):
    return db.query(ExamResult).filter(ExamResult.exam_id == exam_id).all()
 
 
def create_result(db: Session, data: ExamResultCreate):
    result = ExamResult(**data.model_dump())
    db.add(result)
    db.commit()
    db.refresh(result)
    return result
 
 
def update_result(db: Session, result_id: int, data: ExamResultUpdate):
    result = get_result(db, result_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(result, field, value)
    db.commit()
    db.refresh(result)
    return result
 
 
def delete_result(db: Session, result_id: int) -> dict:
    result = get_result(db, result_id)
    db.delete(result)
    db.commit()
    return {"detail": "Exam result deleted"}


def get_my_exam_results(db: Session, current_user_id: int):
    return (
        db.query(ExamResult)
        .filter(ExamResult.student_user_id == current_user_id)
        .all()
    )
 
 
def get_my_result_for_exam(db: Session, exam_id: int, current_user_id: int):
    result = (
        db.query(ExamResult)
        .filter(
            ExamResult.exam_id == exam_id,
            ExamResult.student_user_id == current_user_id,
        )
        .first()
    )
    if not result:
        raise HTTPException(status_code=404, detail="No result found for this exam")
    return result