from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend.schemas.course import CourseCreate, CourseUpdate, CourseResponse
import Backend.crud.course as crud

router = APIRouter(prefix="/courses", tags=["courses"])


@router.post("/", response_model=CourseResponse, status_code=status.HTTP_201_CREATED)
def create_course_endpoint(data: CourseCreate, db: Session = Depends(get_db)):

    course = crud.course_create(db, data)

    return course


@router.put("/{course_name}", response_model=CourseResponse)
def update_department(course_name: str, data: CourseUpdate, db: Session = Depends(get_db)):
    course = crud.update_department(db, course_name, data)

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


@router.get("/{course_name}", response_model=CourseResponse)
def get_course(course_name: str, db: Session = Depends(get_db)):
    course = crud.get_course(db, course_name)

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return course


@router.delete("/{course_name}", status_code=status.HTTP_200_OK)
def delete_course(course_name: str, db: Session = Depends(get_db)):
    course = crud.delete_course(db, course_name)

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    return {"message": "Course deleted successfully"}