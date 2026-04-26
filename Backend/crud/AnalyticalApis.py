from sqlalchemy.orm import Session
from Backend.models import Student, Attendance, CourseOffering, Enrollment, Course, Department, AcademicSemester, Ticket

def get_students(db: Session, page: int, page_size: int):
    query = db.query(Student)
    return query.order_by(Student.user_id).offset((page - 1) * page_size).limit(page_size).all()



def get_attendance(db: Session, page: int, page_size: int):
    query = db.query(Attendance)
    return query.order_by(Attendance.id).offset((page - 1) * page_size).limit(page_size).all()



def get_course_offering(db: Session, page: int, page_size: int):
    query = db.query(CourseOffering)
    return query.order_by(CourseOffering.id).offset((page - 1) * page_size).limit(page_size).all()



def get_enrollments(db: Session, page: int, page_size: int):
    query = db.query(Enrollment)
    return query.order_by(Enrollment.id).offset((page - 1) * page_size).limit(page_size).all()



def get_department(db: Session, page: int, page_size: int):
    query = db.query(Department)
    return query.order_by(Department.id).offset((page - 1) * page_size).limit(page_size).all()



def get_course(db: Session, page: int, page_size: int):
    query = db.query(Course)
    return query.order_by(Course.id).offset((page - 1) * page_size).limit(page_size).all()



def get_academic_semester(db: Session, page: int, page_size: int):
    query = db.query(AcademicSemester)
    return query.order_by(AcademicSemester.id).offset((page - 1) * page_size).limit(page_size).all()



def get_tickets(db: Session, page: int, page_size: int):
    query = db.query(Ticket)
    return query.order_by(Ticket.id).offset((page - 1) * page_size).limit(page_size).all()

