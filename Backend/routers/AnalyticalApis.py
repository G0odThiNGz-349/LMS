from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from Backend.database import get_db
from Backend.schemas.AnalyticalAPis import PaginatedResponse, ExportAttendance, ExportStudent, ExportCourseOffering, ExportEnrollment, ExportCourse, ExportDepartment, ExportAcademicSemester, ExportTickets, ExportExam, ExportExamResult, ExportProfessor, ExportQuiz, ExportQuizSubmission
from Backend.crud.AnalyticalApis import get_students, get_attendance, get_course_offering, get_enrollments, get_course, get_department, get_academic_semester, get_tickets, get_quiz_submissions, get_exams, get_exam_results, get_professors, get_quizzes
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


quiz_submissions_router = APIRouter(prefix="/export_quiz_submissions",tags=["AnalyticalApis"])

@quiz_submissions_router.get(
    "/",
    response_model=PaginatedResponse[ExportQuizSubmission]
)
def list_quiz_submissions(page_size: int = Query(10, ge=1, le=10000), db: Session = Depends(get_db), last_max_id: Optional[int] = Query(None)):
    quiz_submissions = get_quiz_submissions(db, page_size, last_max_id)

    return {
        "page_size": page_size,
        "data": quiz_submissions
    }



exams_router = APIRouter(prefix="/export_exams", tags=["AnalyticalApis"])

@exams_router.get("/", response_model=PaginatedResponse[ExportExam])
def list_exams(page_size: int = Query(10, ge=1, le=10000), db: Session = Depends(get_db), last_max_id: Optional[int] = Query(None)):
    exams = get_exams(db, page_size, last_max_id)

    return {
        "page_size": page_size,
        "data": exams
    }



exam_results_router = APIRouter(prefix="/export_exam_results", tags=["AnalyticalApis"])

@exam_results_router.get("/", response_model=PaginatedResponse[ExportExamResult])
def list_exam_results(page_size: int = Query(10, ge=1, le=10000), db: Session = Depends(get_db), last_max_id: Optional[int] = Query(None)):
    exam_results = get_exam_results(db, page_size, last_max_id)

    return {
        "page_size": page_size,
        "data": exam_results
    }



professors_router = APIRouter(prefix="/export_professors", tags=["AnalyticalApis"])

@professors_router.get("/", response_model=PaginatedResponse[ExportProfessor])
def list_professors(page_size: int = Query(10, ge=1, le=10000), db: Session = Depends(get_db), last_max_id: Optional[int] = Query(None)):
    professors = get_professors(db, page_size, last_max_id)

    return {
        "page_size": page_size,
        "data": professors
    }


quizzes_router = APIRouter(prefix="/export_quizzes", tags=["AnalyticalApis"])

@quizzes_router.get("/", response_model=PaginatedResponse[ExportQuiz])
def list_quizzes(page_size: int = Query(10, ge=1, le=10000), db: Session = Depends(get_db), last_max_id: Optional[int] = Query(None)):
    quizzes = get_quizzes(db, page_size, last_max_id)

    return {
        "page_size": page_size,
        "data": quizzes
    }