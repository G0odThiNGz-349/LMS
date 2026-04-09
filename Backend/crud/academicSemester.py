from sqlalchemy.orm import Session
from Backend.models import AcademicSemester
from Backend.schemas.academicSemester import AcademicSemesterCreate, AcademicSemesterUpdate

def create_academic_semester(db: Session, semester: AcademicSemesterCreate):

    if semester.is_current:
        db.query(AcademicSemester).update({"is_current": False})

    db_semester = AcademicSemester(**semester.model_dump())

    db.add(db_semester)
    db.commit()
    db.refresh(db_semester)

    return db_semester


def update_academic_semester(db: Session, semester_name: str , update: AcademicSemesterUpdate):
    semester = db.query(AcademicSemester).filter(AcademicSemester.name == semester_name).first()

    update_data = update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(semester, key, value)

    db.commit()
    db.refresh(semester)

    return semester


def get_academic_semester(db: Session, semester_name: str):
    return db.query(AcademicSemester).filter(
        AcademicSemester.name == semester_name
    ).first()


def get_all_academic_semesters(db: Session):
    return db.query(AcademicSemester).all()


def get_current_semester(db: Session):
    return db.query(AcademicSemester).filter(
        AcademicSemester.is_current == True
    ).first()


def delete_academic_semester(db: Session, semester_name: str):
    semester = db.query(AcademicSemester).filter(
        AcademicSemester.name == semester_name
    ).first()

    if not semester:
        return None

    db.delete(semester)
    db.commit()

    return semester