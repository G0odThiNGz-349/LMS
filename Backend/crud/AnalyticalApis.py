from sqlalchemy.orm import Session
from Backend.models import Student, Attendance, CourseOffering, Enrollment, Course, Department, AcademicSemester, Ticket
from typing import Optional

def get_students(db: Session, page: int , page_size: int, last_max_id: Optional[int] = None ):
    query = db.query(Student)

    if last_max_id is not None:
        query = query.filter(Student.user_id > last_max_id)

    return (
        query.order_by(Student.user_id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )



def get_attendance(db: Session, page: int , page_size: int, last_max_id: Optional[int] = None ):
    query = db.query(Attendance)

    if last_max_id is not None:
        query = query.filter(Attendance.id > last_max_id)

    return (
        query.order_by(Attendance.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )



def get_course_offering(db: Session, page: int , page_size: int, last_max_id: Optional[int] = None ):
    query = db.query(CourseOffering)

    if last_max_id is not None:
        query = query.filter(CourseOffering.id > last_max_id)

    return (
        query.order_by(CourseOffering.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )



def get_enrollments(db: Session, page: int , page_size: int, last_max_id: Optional[int] = None ):
    query = db.query(Enrollment)

    if last_max_id is not None:
        query = query.filter(Enrollment.id > last_max_id)

    return (
        query.order_by(Enrollment.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )



def get_department(db: Session, page: int, last_max_id: Optional[int] = None, page_size: int = 100):
    query = db.query(Department)

    if last_max_id is not None:
        query = query.filter(Department.id > last_max_id)

    return (
        query.order_by(Department.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )


def get_course(db: Session, page: int, last_max_id: Optional[int] = None, page_size: int = 100):
    query = db.query(Course)

    if last_max_id is not None:
        query = query.filter(Course.id > last_max_id)

    return (
        query.order_by(Course.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )


def get_academic_semester(db: Session, page: int, last_max_id: Optional[int] = None, page_size: int = 100):
    query = db.query(AcademicSemester)

    if last_max_id is not None:
        query = query.filter(AcademicSemester.id > last_max_id)

    return (
        query.order_by(AcademicSemester.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )


def get_tickets(db: Session, page: int, last_max_id: Optional[int] = None, page_size: int = 100):
    query = db.query(Ticket)

    if last_max_id is not None:
        query = query.filter(Ticket.id > last_max_id)

    return (
        query.order_by(Ticket.id)
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

