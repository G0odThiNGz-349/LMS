from sqlalchemy.orm import Session, joinedload
from Backend.models import Course, Department
from Backend.schemas.course import CourseCreate, CourseUpdate
from fastapi import HTTPException


def course_create(db: Session, course: CourseCreate):

    department = db.query(Department).filter(Department.name == course.department_name).first()

    if not department:
            raise HTTPException(
                status_code=404, 
                detail=f"Department with name '{course.department_name}' not found"
            )

    db_course = Course(
        code = course.code,
        name = course.name,
        description = course.description,
        credits = course.credits,
        department_id = department.id
    )

    db.add(db_course)
    db.commit()
    db.refresh(db_course)

    return db_course



def course_update(db: Session, course_name:str, update: CourseUpdate):

    db_course= db.query(Course).filter(Course.name == course_name).first()

    if not db_course:
        raise HTTPException(
            status_code=404,
            detail=f"Course with code '{course_name}' not found"
        )

    update_data = update.model_dump(exclude_unset=True)
    
    if "department_name" in update_data:
            department_name = update_data.pop("department_name")
            
            department = db.query(Department).filter(Department.name == department_name).first()
            
            if not department:
                raise HTTPException(
                    status_code=404,
                    detail=f"Department '{department_name}' not found"
                )
            
            db_course.department_id = department.id

    for key, value in update_data.items():
        setattr(db_course, key, value)

    db.commit()
    db.refresh(db_course)

    db_course = db.query(Course).options(joinedload(Course.department)).filter(Course.code == db_course.code).first()

    return db_course


def get_course(db: Session, course_name: str):
    db_course = db.query(Course).filter(Course.name == course_name).first()

    return db.query(Course).filter(Course.name == course_name).first()