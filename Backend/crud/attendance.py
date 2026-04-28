from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from Backend.models import Attendance, User, CourseOffering, Course, User, Student
from Backend.schemas.attendance import AttendanceCreate
from Backend.auth.dep import get_current_user
from fastapi import Depends


def create_attendance(db: Session,student_user_id: int, course_offering_id: int, session_date, data: AttendanceCreate):
    attendance = Attendance(
        student_user_id=student_user_id,
        course_offering_id=course_offering_id,
        session_date=session_date,
        status=data.status
    )

    db.add(attendance)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Attendance already recorded for this session")

    db.refresh(attendance)
    return attendance




def get_attendance_by_course(db: Session, course_offering_id: int, session_date):
    results = (
        db.query(
            Attendance,
            Student.full_name.label("student_name"),
            Course.name.label("course_name"),
            Course.code.label("course_code"),
        )
        .join(Student, Attendance.student_user_id == Student.user_id)
        .join(CourseOffering, Attendance.course_offering_id == CourseOffering.id)
        .join(Course, CourseOffering.course_id == Course.id)
        .filter(
            Attendance.course_offering_id == course_offering_id,
            Attendance.session_date == session_date
        )
        .all()
    )

    return [
        {
            "student_name": row.student_name,
            "course_name": row.course_name,
            "course_code": row.course_code,
            "session_date": row[0].session_date,
            "status": row[0].status,
            "recorded_at": row[0].recorded_at,
        }
        for row in results
    ]


def delete_attendance(db: Session, attendance_id: int):
    attendance = db.query(Attendance).filter(
        Attendance.id == attendance_id
    ).first()

    if not attendance:
        return None

    db.delete(attendance)
    db.commit()

    return attendance


def get_current_user_attendance(db: Session, current_user: User = Depends(get_current_user)):
    results = (
        db.query(
            Attendance,
            Course.name.label("course_name"),
            Course.code.label("course_code"),
        )
        .join(User, Attendance.student_user_id == User.id)
        .join(CourseOffering, Attendance.course_offering_id == CourseOffering.id)
        .join(Course, CourseOffering.course_id == Course.id)
        .filter(
            Attendance.student_user_id == current_user.id)
        .all()
    )

    return[
        {
            "course_name": row.course_name,
            "course_code": row.course_code,
            "session_date": row.Attendance.session_date,
            "status": row.Attendance.status,
            "recorded_at": row.Attendance.recorded_at
        }
    for row in results
    ]

