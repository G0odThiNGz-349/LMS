from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import date
from Backend.database import get_db
from Backend.schemas.attendance import AttendanceCreate
from Backend.crud.attendance import create_attendance,get_attendance_by_course, delete_attendance

router = APIRouter(
    prefix="/attendance",
    tags=["attendance"],
)


@router.post(
    "/student/{student_user_id}/course/{course_offering_id}/session/{session_date}",
    status_code=status.HTTP_201_CREATED,
)
def create_attendance_route(
    student_user_id: int,
    course_offering_id: int,
    session_date: date,
    data: AttendanceCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_attendance(
            db=db,
            student_user_id=student_user_id,
            course_offering_id=course_offering_id,
            session_date=session_date,
            data=data,
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))


@router.get(
    "/course/{course_offering_id}/session/{session_date}",
    status_code=status.HTTP_200_OK,
)
def get_attendance_by_course_route(
    course_offering_id: int,
    session_date: date,
    db: Session = Depends(get_db),
):
    return get_attendance_by_course(
        db=db,
        course_offering_id=course_offering_id,
        session_date=session_date,
    )


@router.delete("/{attendance_id}", status_code=status.HTTP_200_OK)
def delete_attendance_route(
    attendance_id: int,
    db: Session = Depends(get_db),
):
    deleted = delete_attendance(db=db, attendance_id=attendance_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Attendance record with id {attendance_id} not found.",
        )

    return deleted