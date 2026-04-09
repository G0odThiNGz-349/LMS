from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from Backend.models import Enrollment, CourseOffering, Course, AcademicSemester
from Backend.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate


def create_enrollment(db: Session, data: EnrollmentCreate):
    enrollment = Enrollment(**data.model_dump())

    db.add(enrollment)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Student already enrolled in this course offering")

    db.refresh(enrollment)
    return enrollment


def update_enrollment(db: Session, enrollment_id: int, data: EnrollmentUpdate):
    enrollment = db.query(Enrollment).filter(
        Enrollment.id == enrollment_id
    ).first()

    if not enrollment:
        return None

    update_data = data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(enrollment, key, value)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Duplicate enrollment detected")

    db.refresh(enrollment)
    return enrollment


def get_student_enrollments(db: Session, student_id: int):
    results = (
        db.query(
            Enrollment,
            Course.name.label("course_name"),
            Course.code.label("course_code"),
            AcademicSemester.name.label("semester_name"),
        )
        .join(CourseOffering, Enrollment.course_offering_id == CourseOffering.id)
        .join(Course, CourseOffering.course_id == Course.id)
        .join(AcademicSemester, CourseOffering.semester_id == AcademicSemester.id)
        .filter(Enrollment.student_user_id == student_id)
        .all()
    )

    response = []
    for row in results:
        enrollment = row[0]

        response.append({
            "course_offering_id": enrollment.course_offering_id,
            "course_name": row.course_name,
            "course_code": row.course_code,
            "semester_name": row.semester_name,
            "status": enrollment.status,
            "enrolled_at": enrollment.enrolled_at,
            "grade": enrollment.grade
        })

    return response


def delete_enrollment(db: Session, enrollment_id: int):
    enrollment = db.query(Enrollment).filter(
        Enrollment.id == enrollment_id
    ).first()

    if not enrollment:
        return None

    db.delete(enrollment)
    db.commit()

    return enrollment