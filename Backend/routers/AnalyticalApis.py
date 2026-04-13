from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend.schemas.AnalyticalAPis import PaginatedResponse, ExportAttendance, ExportStudent, ExportCourseOffering, ExportEnrollment, ExportCourse, ExportDepartment
from Backend.crud.AnalyticalApis import get_students, get_attendance, get_course_offering, get_enrollments, get_course, get_department




student_router = APIRouter(prefix="/export_students", tags=["Students"])

@student_router.get("/", response_model=PaginatedResponse[ExportStudent])
def list_students(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)
):
    students = get_students(db, page, page_size)

    return {
        "page": page,
        "page_size": page_size,
        "data": students
    }




enrollment_router = APIRouter(prefix="/export_enrollments", tags=["Enrollments"])

@enrollment_router.get("/", response_model=PaginatedResponse[ExportEnrollment])
def list_enrollments(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    enrollments = get_enrollments(db, page, page_size)

    return {
        "page": page,
        "page_size": page_size,
        "data": enrollments
    }




attendance_router = APIRouter(prefix="/export_attendance", tags=["Attendance"])

@attendance_router.get("/", response_model=PaginatedResponse[ExportAttendance])
def list_attendance(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    attendance = get_attendance(db, page, page_size)

    return {
        "page": page,
        "page_size": page_size,
        "data": attendance
    }




course_offering_router = APIRouter(prefix="/export_course_offerings", tags=["CourseOffering"])

@course_offering_router.get("/", response_model=PaginatedResponse[ExportCourseOffering])
def list_course_offerings(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    course_offering = get_course_offering(db, page, page_size)

    return {
        "page": page,
        "page_size": page_size,
        "data": course_offering
    }




course_router = APIRouter(prefix="/export_courses", tags=["Course"])

@course_router.get("/", response_model=PaginatedResponse[ExportCourse])
def list_courses(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    course = get_course(db, page, page_size)

    return {
        "page": page,
        "page_size": page_size,
        "data": course
    }




department_router = APIRouter(prefix="/export_department", tags=["Department"])

@department_router.get("/", response_model=PaginatedResponse[ExportDepartment])
def list_departments(page: int = Query(1, ge=1), page_size: int = Query(10, ge=1, le=100), db: Session = Depends(get_db)):
    department = get_department(db, page, page_size)

    return {
        "page": page,
        "page_size": page_size,
        "data": department
    }