from sqlalchemy.orm import Session
from Backend.models import Student, Attendance, CourseOffering, Enrollment, Course, Department, AcademicSemester, Ticket, Professor, Exam, ExamResult, Quiz, QuizSubmission
from typing import Optional

def get_students(db: Session, page_size: int, last_max_id: Optional[int] = None):
    query = db.query(Student)

    if last_max_id is not None:
        query = query.filter(Student.user_id > last_max_id)

    return (
        query.order_by(Student.user_id.asc())
        .limit(page_size)
        .all()
    )



def get_attendance(db: Session, page_size: int, last_max_id: Optional[int] = None):
    query = db.query(Attendance)

    if last_max_id is not None:
        query = query.filter(Attendance.id > last_max_id)

    return (
        query.order_by(Attendance.id.asc())
        .limit(page_size)
        .all()
    )



def get_course_offering(db: Session, page_size: int, last_max_id: Optional[int] = None):
    query = db.query(CourseOffering)

    if last_max_id is not None:
        query = query.filter(CourseOffering.id > last_max_id)

    return (
        query.order_by(CourseOffering.id.asc())
        .limit(page_size)
        .all()
    )



def get_enrollments(db: Session, page_size: int, last_max_id: Optional[int] = None):
    query = db.query(Enrollment)

    if last_max_id is not None:
        query = query.filter(Enrollment.id > last_max_id)

    return (
        query.order_by(Enrollment.id.asc())
        .limit(page_size)
        .all()
    )



def get_department(db: Session, page_size: int, last_max_id: Optional[int] = None):
    query = db.query(Department)

    if last_max_id is not None:
        query = query.filter(Department.id > last_max_id)

    return (
        query.order_by(Department.id.asc())
        .limit(page_size)
        .all()
    )


def get_course(db: Session, page_size: int, last_max_id: Optional[int] = None):
    query = db.query(Course)

    if last_max_id is not None:
        query = query.filter(Course.id > last_max_id)

    return (
        query.order_by(Course.id.asc())
        .limit(page_size)
        .all()
    )


def get_academic_semester(db: Session, page_size: int, last_max_id: Optional[int] = None):
    query = db.query(AcademicSemester)

    if last_max_id is not None:
        query = query.filter(AcademicSemester.id > last_max_id)

    return (
        query.order_by(AcademicSemester.id.asc())
        .limit(page_size)
        .all()
    )


def get_tickets(db: Session, page_size: int, last_max_id: Optional[int] = None):
    query = db.query(Ticket)

    if last_max_id is not None:
        query = query.filter(Ticket.id > last_max_id)

    return (
        query.order_by(Ticket.id.asc())
        .limit(page_size)
        .all()
    )


def get_quiz_submissions(
    db: Session,
    page_size: int,
    last_max_id: Optional[int] = None
):
    query = db.query(QuizSubmission)

    if last_max_id is not None:
        query = query.filter(QuizSubmission.id > last_max_id)

    return (
        query.order_by(QuizSubmission.id.asc())
        .limit(page_size)
        .all()
    )



def get_exams(
    db: Session,
    page_size: int,
    last_max_id: Optional[int] = None
):
    query = db.query(Exam)

    if last_max_id is not None:
        query = query.filter(Exam.id > last_max_id)

    return (
        query.order_by(Exam.id.asc())
        .limit(page_size)
        .all()
    )



def get_exam_results(
    db: Session,
    page_size: int,
    last_max_id: Optional[int] = None
):
    query = db.query(ExamResult)

    if last_max_id is not None:
        query = query.filter(ExamResult.id > last_max_id)

    return (
        query.order_by(ExamResult.id.asc())
        .limit(page_size)
        .all()
    )



def get_professors(
    db: Session,
    page_size: int,
    last_max_id: Optional[int] = None
):
    query = db.query(Professor)

    if last_max_id is not None:
        query = query.filter(Professor.user_id > last_max_id)

    return (
        query.order_by(Professor.user_id.asc())
        .limit(page_size)
        .all()
    )



def get_quizzes(
    db: Session,
    page_size: int,
    last_max_id: Optional[int] = None
):
    query = db.query(Quiz)

    if last_max_id is not None:
        query = query.filter(Quiz.id > last_max_id)

    return (
        query.order_by(Quiz.id.asc())
        .limit(page_size)
        .all()
    )