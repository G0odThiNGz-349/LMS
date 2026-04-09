from sqlalchemy.orm import Session
from Backend.models import CourseOffering
from Backend.schemas.courseOffering import CourseofferingCreate, CourseofferingUpdate


def create_course_offering(db: Session, data: CourseofferingCreate):
    obj = CourseOffering(**data.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_course_offering(db: Session, offering_id: int):
    return db.query(CourseOffering).filter(CourseOffering.id == offering_id).first()


def get_all_course_offerings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(CourseOffering).offset(skip).limit(limit).all()


def update_course_offering(db: Session, offering_id: int, update: CourseofferingUpdate):
    obj = db.query(CourseOffering).filter(CourseOffering.id == offering_id).first()
    
    if not obj:
        return None

    update_data = update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(obj, key, value)

    db.commit()
    db.refresh(obj)
    return obj


def delete_course_offering(db: Session, offering_id: int):
    obj = db.query(CourseOffering).filter(CourseOffering.id == offering_id).first()

    if not obj:
        return None

    db.delete(obj)
    db.commit()
    return obj