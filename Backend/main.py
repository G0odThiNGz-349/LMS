from fastapi import FastAPI
from Backend.database import engine
from Backend.models import Base
from Backend.routers import combiend, department, course , AnalyticalApis, ticket, coursePrerequisite, enrollment, attendance, academicSemester, courseOffering

app = FastAPI()


Base.metadata.create_all(bind=engine)

app.include_router(combiend.router)
app.include_router(department.router)
app.include_router(course.router)
app.include_router(ticket.router)
app.include_router(courseOffering.router)
app.include_router(attendance.router)
app.include_router(enrollment.router)
app.include_router(coursePrerequisite.router)
app.include_router(academicSemester.router)
app.include_router(AnalyticalApis.student_router)
app.include_router(AnalyticalApis.attendance_router)
app.include_router(AnalyticalApis.course_offering_router)
app.include_router(AnalyticalApis.enrollment_router)
app.include_router(AnalyticalApis.department_router)
app.include_router(AnalyticalApis.course_router)
app.include_router(AnalyticalApis.tickets_router)
app.include_router(AnalyticalApis.academic_semester_router)