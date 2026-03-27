from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Enum, DateTime, Date, Text, Boolean, JSON, UniqueConstraint, TIMESTAMP, func
from sqlalchemy.orm import relationship
from database import Base  
import enum


class UserRole(enum.Enum):
    student = "student"
    professor = "professor"
    teaching_assistant = "teaching_assistant"
    academic_affair = "academic_affair"
    admin = "admin"
    it_staff = "it_staff"

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

class TicketStatus(enum.Enum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"

class AcademicYear(enum.Enum):
    freshman= "freshman"
    sophomore= "sophomore"
    junior= "junior"
    senior_1= "senior_1"
    senior_2= "senior_2"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    university_id = Column(String(30), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    is_active = Column(Boolean, default=True)
    login_count = Column(Integer,default=0, nullable=False)
    last_login = Column(TIMESTAMP, nullable=True)
    last_login_ip = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.current_timestamp())
    updated_at = Column(TIMESTAMP, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    student = relationship("Student", uselist=False, back_populates="user", cascade="all, delete-orphan")
    professor = relationship("Professor", uselist=False, back_populates="user", cascade="all, delete-orphan")


class Student(Base):
    __tablename__ = "students"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    full_name = Column(String(255), nullable=False)
    national_id = Column(String(20), unique=True, nullable=False)
    phone = Column(String(20), nullable=False)
    birth_date = Column(Date, nullable=False)
    address = Column(Text)
    enroll_date = Column(Date, nullable=False)
    expected_graduation = Column(Date)          
    academic_year = Column(Enum(AcademicYear))          
    current_gpa = Column(Numeric(3, 2), default=0.00)

    user = relationship("User", back_populates="student")

class Professor(Base):
    __tablename__ = "professors"

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    full_name = Column(String(255), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))
    hire_date = Column(Date)
    role= Column(String(30))

    user = relationship("User", back_populates="professor")
    department = relationship("Department", back_populates="professors")


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)
    head_prof_user_id = Column(Integer, ForeignKey("users.id"))

    head_professor = relationship("User", foreign_keys=[head_prof_user_id])
    professors = relationship("Professor", back_populates="department")


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(30), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    credits = Column(Integer, nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"))

    department = relationship("Department")


class CoursePrerequisite(Base):
    __tablename__ = "course_prerequisites"

    course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)
    prerequisite_course_id = Column(Integer, ForeignKey("courses.id"), primary_key=True)


class AcademicSemester(Base):
    __tablename__ = "academic_semesters"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    is_current = Column(Boolean, default=False)


class CourseOffering(Base):
    __tablename__ = "course_offerings"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    semester_id = Column(Integer, ForeignKey("academic_semesters.id"), nullable=False)
    professor_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_date = Column(Date)
    end_date = Column(Date)

    course = relationship("Course")
    semester = relationship("AcademicSemester")
    professor = relationship("User")


class Enrollment(Base):
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_offering_id = Column(Integer, ForeignKey("course_offerings.id"), nullable=False)
    grade = Column(Numeric(3, 2))
    status = Column(Enum(EnrollmentStatus), default=EnrollmentStatus.active)
    enrolled_at = Column(DateTime, server_default=func.current_timestamp())

    __table_args__ = (
        UniqueConstraint('student_user_id', 'course_offering_id', name='uq_enrollment'),
    )


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_offering_id = Column(Integer, ForeignKey("course_offerings.id"), nullable=False)
    session_date = Column(Date, nullable=False)
    status = Column(Enum(AttendanceStatus), nullable=False)
    recorded_at = Column(DateTime, server_default=func.current_timestamp())

    __table_args__ = (
        UniqueConstraint('student_user_id', 'course_offering_id', 'session_date'),
    )


class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(Text)
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    assigned_to_user_id = Column(Integer, ForeignKey("users.id"))
    status = Column(Enum(TicketStatus), default=TicketStatus.open)
    created_at = Column(DateTime, server_default=func.current_timestamp())
    updated_at = Column(DateTime, server_default=func.current_timestamp(), onupdate=func.current_timestamp())

    created_by = relationship("User", foreign_keys=[created_by_user_id])
    assigned_to = relationship("User", foreign_keys=[assigned_to_user_id])


class Resource(Base):
    __tablename__ = "resources"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_offering_id = Column(Integer, ForeignKey("course_offerings.id"))
    title = Column(String(255), nullable=False)
    file_url = Column(Text)
    resource_type = Column(String(50))
    uploaded_by_user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, server_default=func.current_timestamp())


class Quiz(Base):
    __tablename__ = "quizzes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    course_offering_id = Column(Integer, ForeignKey("course_offerings.id"))
    title = Column(String(255), nullable=False)
    total_marks = Column(Numeric(5, 2))
    due_date = Column(DateTime)
    created_at = Column(DateTime, server_default=func.current_timestamp())


class QuizSubmission(Base):
    __tablename__ = "quiz_submissions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    quiz_id = Column(Integer, ForeignKey("quizzes.id"))
    student_user_id = Column(Integer, ForeignKey("users.id"))
    score = Column(Numeric(5, 2))
    submitted_at = Column(DateTime, server_default=func.current_timestamp())


class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, autoincrement=True)
    topic = Column(String(100), nullable=False)         
    sender_user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text, nullable=False)
    sent_at = Column(DateTime, server_default=func.current_timestamp())

    sender = relationship("User")


class StudentPerformanceLog(Base):
    __tablename__ = "student_performance_logs"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    course_offering_id = Column(Integer, ForeignKey("course_offerings.id"))
    event_type = Column(String(50), nullable=False)
    event_value = Column(Numeric(5, 2))
    extra_data = Column(JSON)
    recorded_at = Column(DateTime, server_default=func.current_timestamp())