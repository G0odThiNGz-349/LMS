from sqlalchemy.orm import Session
from Backend.models import Student, Attendance, CourseOffering, Enrollment, Course, Department

def get_students(db: Session, page: int, page_size: int):
    query = db.query(Student)
    return query.offset((page - 1) * page_size).limit(page_size).all()



def get_attendance(db: Session, page: int, page_size: int):
    query = db.query(Attendance)
    return query.offset((page - 1) * page_size).limit(page_size).all()



def get_course_offering(db: Session, page: int, page_size: int):
    query = db.query(CourseOffering)
    return query.offset((page - 1) * page_size).limit(page_size).all()



def get_enrollments(db: Session, page: int, page_size: int):
    query = db.query(Enrollment)
    return query.offset((page - 1) * page_size).limit(page_size).all()


def get_department(db: Session, page: int, page_size: int):
    query = db.query(Department)
    return query.offset((page - 1) * page_size).limit(page_size).all()


def get_course(db: Session, page: int, page_size: int):
    query = db.query(Course)
    return query.offset((page - 1) * page_size).limit(page_size).all()