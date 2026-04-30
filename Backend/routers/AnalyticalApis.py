from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend.schemas.AnalyticalAPis import PaginatedResponse, ExportAttendance, ExportStudent, ExportCourseOffering, ExportEnrollment, ExportCourse, ExportDepartment, ExportAcademicSemester, ExportTickets
from Backend.crud.AnalyticalApis import get_students, get_attendance, get_course_offering, get_enrollments, get_course, get_department, get_academic_semester, get_tickets
from typing import Optional




student_router = APIRouter(prefix="/export_students", tags=["AnalyticalApis"])

@student_router.get("/", response_model=PaginatedResponse[ExportStudent])
def list_students(page_size: int = Query(10, ge=1, le=10000), db: Session = Depends(get_db), last_max_id: Optional[int] = Query(None)):
    students = get_students(db, page_size, last_max_id)

    return {
        "page_size": page_size,
        "data": students
    }




enrollment_router = APIRouter(prefix="/export_enrollments", tags=["AnalyticalApis"])

@enrollment_router.get("/", response_model=PaginatedResponse[ExportEnrollment])
def list_enrollments(page_size: int = Query(10, ge=1, le=10000), db: Session = Depends(get_db), last_max_id: Optional[int] = Query(None)):
    enrollments = get_enrollments(db, page_size, last_max_id)

    return {
        "page_size": page_size,
        "data": enrollments
    }




attendance_router = APIRouter(prefix="/export_attendance", tags=["AnalyticalApis"])

@attendance_router.get("/", response_model=PaginatedResponse[ExportAttendance])
def list_attendance(page_size: int = Query(10, ge=1, le=10000), db: Session = Depends(get_db), last_max_id: Optional[int] = Query(None)):
    attendance = get_attendance(db, page_size, last_max_id)

    return {
        "page_size": page_size,
        "data": attendance
    }




course_offering_router = APIRouter(prefix="/export_course_offerings", tags=["AnalyticalApis"])

@course_offering_router.get("/", response_model=PaginatedResponse[ExportCourseOffering])
def list_course_offerings(page_size: int = Query(10, ge=1, le=10000), db: Session = Depends(get_db), last_max_id: Optional[int] = Query(None)):
    course_offering = get_course_offering(db, page_size, last_max_id)

    return {
        "page_size": page_size,
        "data": course_offering
    }




course_router = APIRouter(prefix="/export_courses", tags=["AnalyticalApis"])

@course_router.get("/", response_model=PaginatedResponse[ExportCourse])
def list_courses(page_size: int = Query(10, ge=1, le=10000), db: Session = Depends(get_db), last_max_id: Optional[int] = Query(None)):
    course = get_course(db, page_size, last_max_id)

    return {
        "page_size": page_size,
        "data": course
    }




department_router = APIRouter(prefix="/export_department", tags=["AnalyticalApis"])

@department_router.get("/", response_model=PaginatedResponse[ExportDepartment])
def list_departments(page_size: int = Query(10, ge=1, le=10000), db: Session = Depends(get_db), last_max_id: Optional[int] = Query(None)):
    department = get_department(db, page_size, last_max_id)

    return {
        "page_size": page_size,
        "data": department
    }



academic_semester_router = APIRouter(prefix="/export_academic_semester", tags=["AnalyticalApis"])

@academic_semester_router.get("/", response_model=PaginatedResponse[ExportAcademicSemester])
def list_academic_semester(page_size: int = Query(10, ge=1, le=10000), db: Session = Depends(get_db), last_max_id: Optional[int] = Query(None)):
    academic_semester = get_academic_semester(db, page_size, last_max_id)

    return {
        "page_size": page_size,
        "data": academic_semester
    }




tickets_router = APIRouter(prefix="/export_tickets", tags=["AnalyticalApis"])

@tickets_router.get("/", response_model=PaginatedResponse[ExportTickets])
def list_tickets(page_size: int = Query(10, ge=1, le=10000), db: Session = Depends(get_db), last_max_id: Optional[int] = Query(None)):
    tickets = get_tickets(db, page_size, last_max_id)

    return {
        "page_size": page_size,
        "data": tickets
    }
