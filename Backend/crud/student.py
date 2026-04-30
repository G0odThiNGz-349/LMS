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
    student= db.query(Student).options(
        joinedload(Student.user)
    ).join(Student.user).filter(
        User.university_id == university_id
    ).first()
    return{
        "full_name": student.full_name,
        "national_id": student.national_id,
        "phone": student.phone,
        "birth_date": student.birth_date,
        "address": student.address,
        "enroll_date": student.enroll_date,
        "expected_graduation": student.expected_graduation,
        "academic_year": student.academic_year,
        "current_gpa": student.current_gpa,
        "university_id": student.user.university_id,
        "email": student.user.email,
    }



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


def get_students(db: Session, page: int = 1, page_size: int = 100):
    query = db.query(Student)
    response =query.order_by(Student.user_id).offset((page - 1) * page_size).limit(page_size).all()
    return[{
        "user_id": row.user_id,
        "university_id": row.user.university_id,
        "full_name": row.full_name,
        "academic_year": row.academic_year,
        "current_gpa": row.current_gpa
    }
    for row in response
    ]




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
    response= db.query(Student).filter(Student.academic_year == academic_year).limit(100)

    return[{
        "user_id": row.user_id,
        "university_id": row.user.university_id,
        "full_name": row.full_name,
        "academic_year": row.academic_year,
        "current_gpa": row.current_gpa
    }
    for row in response
    ]


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