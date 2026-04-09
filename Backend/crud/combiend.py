from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
from Backend.models import Student, User, Professor
from Backend.schemas.combinedCreate import CreateUserStudent, CreateUserProfessor


def create_user_student(db: Session, student: CreateUserStudent ):
    db_user = User(
        university_id = student.university_id,
        email = student.email,
        role = "student",
        password_hash = student.password
    )
    db.add(db_user)
    db.flush()

    db_student = Student(
        user_id = db_user.id,
        full_name = student.full_name,
        national_id = student.national_id,
        phone = student.phone,
        birth_date = student.birth_date,
        address = student.address,
        enroll_date = student.enroll_date,
        expected_graduation = student.expected_graduation,
        academic_year = student.academic_year,
        current_gpa = student.current_gpa
    )

    db.add(db_student)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("the student already exsists")
    db.refresh(db_student)

    return db_student



def create_user_professor(db: Session, professor: CreateUserProfessor ):
    db_user = User(
        university_id = professor.university_id,
        email = professor.email,
        role = professor.role,
        password_hash = professor.password
    )
    db.add(db_user)
    db.flush()

    db_professor = Professor(
        user_id = db_user.id,
        full_name = professor.full_name,
        hire_date = professor.hire_date
    )

    db.add(db_professor)
    db.commit()
    db.refresh(db_professor)

    return db_professor