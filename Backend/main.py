from fastapi import FastAPI
from Backend.database import engine
from Backend.models import Base
from Backend.routers import combiend, department, course , AnalyticalApis, ticket, coursePrerequisite, enrollment, attendance, academicSemester, courseOffering, student, users, quizSubmission, quiz, exam, examResults
from Backend.auth.router import router as auth_router
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()


Base.metadata.create_all(bind=engine)

app.include_router(auth_router)
app.include_router(users.router)
app.include_router(combiend.router)
app.include_router(student.router)
app.include_router(department.router)
app.include_router(course.router)
app.include_router(ticket.router)
app.include_router(courseOffering.router)
app.include_router(attendance.router)
app.include_router(enrollment.router)
app.include_router(coursePrerequisite.router)
app.include_router(academicSemester.router)
app.include_router(quiz.quiz_router)
app.include_router(quizSubmission.my_quiz_router)
app.include_router(quizSubmission.submission_router)
app.include_router(exam.exam_router)
app.include_router(examResults.my_result_router)
app.include_router(examResults.result_router)
app.include_router(AnalyticalApis.student_router)
app.include_router(AnalyticalApis.attendance_router)
app.include_router(AnalyticalApis.course_offering_router)
app.include_router(AnalyticalApis.enrollment_router)
app.include_router(AnalyticalApis.department_router)
app.include_router(AnalyticalApis.course_router)
app.include_router(AnalyticalApis.tickets_router)
app.include_router(AnalyticalApis.academic_semester_router)
app.include_router(AnalyticalApis.quizzes_router)
app.include_router(AnalyticalApis.professors_router)
app.include_router(AnalyticalApis.quiz_submissions_router)
app.include_router(AnalyticalApis.exam_results_router)
app.include_router(AnalyticalApis.exams_router)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500", "http://localhost:5500", "null"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)