from sqlalchemy import Column, Integer, String, ForeignKey, Numeric,Enum, DateTime, Date,Text, Boolean, JSON, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from Database import Base
import enum

class UserRole(enum.Enum):
    student= "student"
    professor = "professor"
    admin = "admin"
    it_staff="it_staff"

class AcademicYear(enum.Enum):
    freshman= "freshman"
    sophomore= "sophomore"
    junior= "junior"
    senior_1= "senior_1"
    senior_2= "senior_2"

class TicketStatus(enum.Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"

class AttendanceStatus(enum.Enum):
    present = "present"
    absent = "absent"
    late = "late"
    excused = "excused"

class EnrollmentStatus(enum.Enum):
    active = "active"
    passed = "passed"
    failed = "failed"
    dropped = "dropped"


class User(Base):
    __tablename__= "users"
    id= Column(Integer, unique=True, primary_key=True, nullable=False)
    email= Column(String(255), unique=True, nullable=False)
    password_hash= Column(String(225), nullable=False)
    role= Column(Enum(UserRole), nullable=False)
    created_at= Column(DateTime, default=func.now())
    updated_at= Column(DateTime, default=func.now(), onupdate=func.now())
    last_login= Column(DateTime)


class Student(Base):
    __tablename__= "students"
    student_id= Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    national_id= Column(String(20), unique=True, nullable=False)
    phone= Column(String(20), nullable=False)
    birth_date=Column(Date, nullable=False)
    address= Column(Text)
    enroll_date= Column(Date, nullable=False)
    excepted_graduation= Column(Date)
    academic_year= Column(Enum(AcademicYear))
    current_gpa= Column(Numeric(3,2))
    created_at= Column(DateTime, default=func.now())

    user = relationship("User")


class Professor(Base):
    __tablename__ = "professors"

    professor_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    full_name = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    hire_date = Column(Date)
    role= Column(String(30))
    created_at = Column(DateTime, default=func.now())

    user = relationship("User")
    department = relationship("Department", back_populates="professors")


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    head_prof_user_id = Column(Integer, ForeignKey("users.id"))

    head_professor = relationship("User", foreign_keys=[head_prof_user_id])
    professors = relationship("Professor", back_populates="department")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    code = Column(String(20), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    credits = Column(Integer)
    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("Department")
    prerequisites = relationship(
        "Course",
        secondary="course_prerequisites",
        primaryjoin="Course.id == CoursePrerequisite.course_id",
        secondaryjoin="Course.id == CoursePrerequisite.prerequisite_course_id"
    )


class CoursePrerequisite(Base):
    __tablename__ = "course_prerequisites"

    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    prerequisite_course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)


class AcademicSemester(Base):
    __tablename__ = "academic_semesters"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_current = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())


class CourseOffering(Base):
    __tablename__ = "course_offerings"

    id = Column(Integer, primary_key=True)
    course_id = Column(Integer, ForeignKey("courses.id"),nullable=False)
    semester_id = Column(Integer, ForeignKey("academic_semesters.id"),nullable=False)
    professor_user_id = Column(Integer, ForeignKey("users.id"),nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)
    created_at = Column(DateTime, default=func.now())

    course = relationship("Course")
    semester = relationship("AcademicSemester")
    professor = relationship("User")


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True)
    student_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_offering_id = Column(Integer, ForeignKey("course_offerings.id"), nullable=False)
    grade = Column(Numeric(3, 2))
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.active)
    enrolled_at = Column(DateTime, default=func.now())

    __table_args__=(
        UniqueConstraint('student_user_id', 'course_offering_id'),
    )

    student = relationship("User")
    course_offering = relationship("CourseOffering")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True)
    student_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_offering_id = Column(Integer, ForeignKey("course_offerings.id"), nullable=False)
    session_date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)
    recorded_at = Column(DateTime, default=func.now())

    __table_args__ = (
    UniqueConstraint('student_user_id', 'course_offering_id', 'session_date'),
    )
    student = relationship("User")
    course_offering = relationship("CourseOffering")


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    assigned_to_user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(TicketStatus), default=TicketStatus.open)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    created_by = relationship("User", foreign_keys=[created_by_user_id])
    assigned_to = relationship("User", foreign_keys=[assigned_to_user_id])


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True)
    course_offering_id = Column(Integer, ForeignKey("course_offerings.id"))
    title = Column(String(255), nullable=False)
    file_url = Column(Text)
    resource_type = Column(String(50))
    uploaded_by_user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())

    course_offering = relationship("CourseOffering")
    uploaded_by = relationship("User")


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True)
    course_offering_id = Column(Integer, ForeignKey("course_offerings.id"))
    title = Column(String(255), nullable=False)
    total_marks = Column(Numeric(5, 2))
    due_date = Column(DateTime)
    created_at = Column(DateTime, default=func.now())

    course_offering = relationship("CourseOffering")


class QuizSubmission(Base):
    __tablename__ = "quiz_submissions"

    id = Column(Integer, primary_key=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    student_user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Numeric(5, 2))
    submitted_at = Column(DateTime, default=func.now())

    quiz = relationship("Quiz")
    student = relationship("User")


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True)
    topic = Column(String(100), nullable=False)
    sender_user_id = Column(Integer, ForeignKey("users.id"))
    receiver_room_id= Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime, default=func.now())

    sender = relationship("User")


class StudentPerformanceLog(Base):
    __tablename__ = "student_performance_logs"

    id = Column(Integer, primary_key=True)
    student_user_id = Column(Integer, ForeignKey("users.id"))
    course_offering_id = Column(Integer, ForeignKey("course_offerings.id"))
    event_type = Column(String(50), nullable=False)
    event_value = Column(Numeric(5, 2))
    extra_data = Column(JSON)
    recorded_at = Column(DateTime, default=func.now())

    student = relationship("User")
    course_offering = relationship("CourseOffering")
