from sqlalchemy.orm import Session, joinedload
from Backend.models import Student, User
from Backend.schemas.student import StudentCreate, StudentAdminUpdate
from Backend.auth.dep import get_current_user
from fastapi import Depends


def create_student(db: Session, student: StudentCreate):
    db_student = Student(**student.model_dump())
    
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    
    return db_student


def get_student(db: Session, university_id: str):
    return db.query(Student).options(
        joinedload(Student.user)
    ).join(Student.user).filter(
        User.university_id == university_id
    ).first()


def get_current_student(db: Session, current_user: User = Depends(get_current_user)):
    current_student = db.query(Student).options(
        joinedload(Student.user)
    ).filter(Student.user_id == current_user.id).first()

    return{
        "full_name": current_student.full_name,
        "national_id": current_student.national_id,
        "phone": current_student.phone,
        "birth_date": current_student.birth_date,
        "address": current_student.address,
        "enroll_date": current_student.enroll_date,
        "expected_graduation": current_student.expected_graduation,
        "academic_year": current_student.academic_year,
        "current_gpa": current_student.current_gpa,
        "university_id": current_student.user.university_id,
        "email": current_student.user.email,
    }


def get_students(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Student).offset(skip).limit(limit).all()


def search_students_by_university_id(db: Session, query: str):
    return (
        db.query(Student)
        .options(joinedload(Student.user))
        .join(Student.user)
        .filter(User.university_id.ilike(f"%{query}%"))
        .all()
    )


def search_students_by_full_name(db: Session, query: str):
    return db.query(Student).filter(
        Student.full_name.ilike(f"%{query}%")
    ).all()


def get_students_by_year(db: Session, academic_year: str):
    return db.query(Student).filter(Student.academic_year == academic_year).all()


def update_student_by_university_id(db: Session, university_id: str, updates: StudentAdminUpdate):
    student = db.query(Student).join(Student.user).filter(
        User.university_id == university_id
    ).first()

    if not student:
        return None

    update_data = updates.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(student, key, value)

    db.commit()
    db.refresh(student)

    return student


def delete_student_by_university_id(db: Session, university_id: str):
    student = db.query(Student).join(Student.user).filter(
        User.university_id == university_id
    ).first()

    if not student:
        return None

    db.delete(student)
    db.commit()

    return student