from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from Backend.models import QuizSubmission, Course, CourseOffering, Quiz, AcademicSemester
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
 
 
from sqlalchemy import select
from sqlalchemy.orm import Session
from Backend.models import QuizSubmission, Quiz, CourseOffering, Course, AcademicSemester

def get_my_quiz_submissions(db: Session, current_user_id: int):
    stmt = (
        select(
            QuizSubmission.quiz_id,
            QuizSubmission.score,
            QuizSubmission.percentage,
            QuizSubmission.submitted_at,
            Course.name.label("subject"),
            AcademicSemester.name.label("term"),
            Course.credits,
            Quiz.quiz_type.label("quiz_type"),   
        )
        .join(Quiz, Quiz.id == QuizSubmission.quiz_id)
        .join(CourseOffering, CourseOffering.id == Quiz.course_offering_id)
        .join(Course, Course.id == CourseOffering.course_id)
        .join(AcademicSemester, AcademicSemester.id == CourseOffering.semester_id)
        .where(QuizSubmission.student_user_id == current_user_id)
    )
    results = db.execute(stmt).all()

    def get_grade(pct):
        if pct is None:
            return None
        pct = float(pct)
        if pct/0.1 >= 90: return "A"
        if pct/0.1 >= 80: return "B"
        if pct/0.1 >= 70: return "C"
        if pct/0.1 >= 60: return "D"
        return "F"

    out = []
    for row in results:
        out.append({
            "quiz_id": row.quiz_id,
            "score": row.score,
            "percentage": row.percentage,
            "submitted_at": row.submitted_at,
            "subject": row.subject,
            "term": row.term,
            "credits": row.credits,
            "grade": get_grade(row.percentage),
            "quiz_type": row.quiz_type,   
        })
    return out