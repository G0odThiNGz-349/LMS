from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend.schemas.courseOffering import CourseofferingCreate, CourseofferingUpdate
from Backend.crud.courseOffering import create_course_offering, get_course_offering, get_all_course_offerings, update_course_offering, delete_course_offering

router = APIRouter(
    prefix="/course-offerings",
    tags=["course-offerings"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_course_offering_route(
    data: CourseofferingCreate,
    db: Session = Depends(get_db),
):

    return create_course_offering(db=db, data=data)


@router.get("/", status_code=status.HTTP_200_OK)
def get_all_course_offerings_route(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):

    return get_all_course_offerings(db=db, skip=skip, limit=limit)


@router.get("/{offering_id}", status_code=status.HTTP_200_OK)
def get_course_offering_route(
    offering_id: int,
    db: Session = Depends(get_db),
):

    offering = get_course_offering(db=db, offering_id=offering_id)

    if not offering:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course offering with id {offering_id} not found.",
        )

    return offering


@router.patch("/{offering_id}", status_code=status.HTTP_200_OK)
def update_course_offering_route(
    offering_id: int,
    data: CourseofferingUpdate,
    db: Session = Depends(get_db),
):
    updated = update_course_offering(db=db, offering_id=offering_id, update=data)

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course offering with id {offering_id} not found.",
        )

    return updated


@router.delete("/{offering_id}", status_code=status.HTTP_200_OK)
def delete_course_offering_route(
    offering_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_course_offering(db=db, offering_id=offering_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Course offering with id {offering_id} not found.",
        )

    return deleted