from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException
from Backend.models import ExamResult, Course, Exam, AcademicSemester, CourseOffering
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
    stmt = (
        select(
            ExamResult.exam_id,
            ExamResult.score,
            ExamResult.percentage,
            Course.name.label("subject"),
            AcademicSemester.name.label("term"),
            Course.credits,
            Exam.exam_type.label("exam_type"), 
        )
        .join(Exam, Exam.id == ExamResult.exam_id)
        .join(CourseOffering, CourseOffering.id == Exam.course_offering_id)
        .join(Course, Course.id == CourseOffering.course_id)
        .join(AcademicSemester, AcademicSemester.id == CourseOffering.semester_id)
        .where(ExamResult.student_user_id == current_user_id)
    )
    results = db.execute(stmt).all()

    def get_grade(pct):
        if pct is None:
            return None

        pct = float(pct)
        if (pct+60) >= 90: return "A"
        if (pct+60) >= 80: return "B"
        if (pct+60) >= 70: return "C"
        if (pct+60) >= 60: return "D"
        return "F"  

    out = []
    for row in results:
        out.append({
            "exam_id": row.exam_id,
            "score": row.score,
            "percentage": row.percentage,
            "subject": row.subject,
            "term": row.term,
            "credits": row.credits,
            "grade": get_grade(row.score),
            "exam_type": row.exam_type,   
        })
    return out
 
 
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