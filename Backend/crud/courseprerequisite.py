from sqlalchemy.orm import Session
from Backend.models import Course, CoursePrerequisite
from Backend.schemas.coursePrerequisites import CoursePrerequisitesCreate, CoursePrerequisitesUpdate
from fastapi import HTTPException

def create_course_prerequisite(db: Session, course: CoursePrerequisitesCreate):
    course_db=db.query(Course).filter(Course.name == course.course_name).first()
    prerequisite_db=db.query(Course).filter(Course.name == course.prerequisite_course_name).first()

    if not course_db:
        raise HTTPException(
            status_code=404,
            detail=f"Course with name {course.course_name} not found"
        )

    if not prerequisite_db:
        raise HTTPException(
            status_code=404,
            detail=f"Course with name {course.prerequisite_course_name} not found"
        )
    

    db_course_prerequisite = CoursePrerequisite(
        course_id = course_db.id,
        prerequisite_course_id = prerequisite_db.id
    )

    db.add(db_course_prerequisite)
    db.commit()
    db.refresh(db_course_prerequisite)
    return db_course_prerequisite


def update_course_prerequisite(db: Session, course_name: str, prerequisite_course_name: str, update: CoursePrerequisitesUpdate):
   
    course_db = db.query(Course).filter(
        Course.name == course_name
    ).first()

    if not course_db:
        raise HTTPException(
            status_code=404,
            detail=f"Course with name {course_name} not found"
        )


    prerequisite_db = db.query(Course).filter(
        Course.name == prerequisite_course_name
    ).first()

    if not prerequisite_db:
        raise HTTPException(
            status_code=404,
            detail=f"Course with name {prerequisite_course_name} not found"
        )

  
    db_course_prerequisite = db.query(CoursePrerequisite).filter(
        CoursePrerequisite.course_id == course_db.id,
        CoursePrerequisite.prerequisite_course_id == prerequisite_db.id
    ).first()

    if not db_course_prerequisite:
        raise HTTPException(
            status_code=404,
            detail="Course prerequisite relation not found"
        )


    if update.course_name is not None:
        new_course = db.query(Course).filter(
            Course.name == update.course_name
        ).first()

        if not new_course:
            raise HTTPException(
                status_code=404,
                detail=f"Course with name {update.course_name} not found"
            )

        db_course_prerequisite.course_id = new_course.id


    if update.prerequisite_course_name is not None:
        new_prereq = db.query(Course).filter(
            Course.name == update.prerequisite_course_name
        ).first()

        if not new_prereq:
            raise HTTPException(
                status_code=404,
                detail=f"Course with name {update.prerequisite_course_name} not found"
            )

        db_course_prerequisite.prerequisite_course_id = new_prereq.id

    db.commit()
    db.refresh(db_course_prerequisite)

    return db_course_prerequisite