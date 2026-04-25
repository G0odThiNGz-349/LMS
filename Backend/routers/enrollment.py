from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend.schemas.enrollment import EnrollmentCreate, EnrollmentUpdate
from Backend.crud.enrollment import create_enrollment, update_enrollment, get_student_enrollments, delete_enrollment


router = APIRouter(
    prefix="/enrollments",
    tags=["enrollments"],
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_enrollment_route(
    data: EnrollmentCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_enrollment(db=db, data=data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.patch("/{enrollment_id}", status_code=status.HTTP_200_OK)
def update_enrollment_route(
    enrollment_id: int,
    data: EnrollmentUpdate,
    db: Session = Depends(get_db),
):
    try:
        updated = update_enrollment(db=db, enrollment_id=enrollment_id, data=data)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

    if not updated:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment with id {enrollment_id} not found.",
        )

    return updated


@router.get("/student/{student_id}", status_code=status.HTTP_200_OK)
def get_student_enrollments_route(
    student_id: int,
    db: Session = Depends(get_db),
):
    return get_student_enrollments(db=db, student_id=student_id)


@router.delete("/{enrollment_id}", status_code=status.HTTP_200_OK)
def delete_enrollment_route(
    enrollment_id: int,
    db: Session = Depends(get_db),
):

    deleted = delete_enrollment(db=db, enrollment_id=enrollment_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment with id {enrollment_id} not found.",
        )

    return deleted