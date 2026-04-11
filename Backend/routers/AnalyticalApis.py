from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend.schemas.AnalyticalAPis import PaginatedResponse, ExportAttendance, ExportStudent, ExportCourseOffering, ExportEnrollment
from Backend.crud.AnalyticalApis import get_students, get_attendance, get_course_offering, get_enrollments




student_router = APIRouter(prefix="/students", tags=["Students"])

@student_router.get("/", response_model=PaginatedResponse[ExportStudent])
def list_students(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)
):
    students = get_students(db, page, page_size)

    return {
        "page": page,
        "page_size": page_size,
        "data": students
    }




enrollment_router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

@enrollment_router.get("/", response_model=PaginatedResponse[ExportEnrollment])
def list_enrollments(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    students = get_enrollments(db, page, page_size)

    return {
        "page": page,
        "page_size": page_size,
        "data": students
    }




attendance_router = APIRouter(prefix="/attendance", tags=["Attendance"])

@attendance_router.get("/", response_model=PaginatedResponse[ExportAttendance])
def list_attendance(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    students = get_attendance(db, page, page_size)

    return {
        "page": page,
        "page_size": page_size,
        "data": students
    }




course_offering_router = APIRouter(prefix="/course_offerings", tags=["CourseOffering"])

@course_offering_router.get("/", response_model=PaginatedResponse[ExportCourseOffering])
def list_course_offerings(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    students = get_course_offering(db, page, page_size)

    return {
        "page": page,
        "page_size": page_size,
        "data": students
    }