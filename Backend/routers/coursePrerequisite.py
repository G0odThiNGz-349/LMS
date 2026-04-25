from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend.schemas.coursePrerequisites import CoursePrerequisitesCreate, CoursePrerequisitesUpdate
from Backend.crud.coursePrerequisite import create_course_prerequisite, update_course_prerequisite

router = APIRouter(
    prefix="/course-prerequisites",
    tags=["course-prerequisites"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_course_prerequisite_route(
    data: CoursePrerequisitesCreate,
    db: Session = Depends(get_db),
):
    return create_course_prerequisite(db=db, course=data)


@router.patch(
    "/course/{course_name}/prerequisite/{prerequisite_course_name}",
    status_code=status.HTTP_200_OK,
)
def update_course_prerequisite_route(
    course_name: str,
    prerequisite_course_name: str,
    data: CoursePrerequisitesUpdate,
    db: Session = Depends(get_db),
):
    return update_course_prerequisite(
        db=db,
        course_name=course_name,
        prerequisite_course_name=prerequisite_course_name,
        update=data,
    )