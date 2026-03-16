from sqlalchemy import Column, Integer, String, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(80))


    enrollments = relationship(
        "Enrollment",
        back_populates="student",
        cascade="all, delete-orphan"
    )
    courses = relationship(
        "Course",
        secondary="enrollments",
        viewonly=True
    )


class Course(Base):
    __tablename__ = "courses"

    id = Column(String(30), primary_key=True)
    course_name = Column(String(50))
    sessions = Column(Integer)


    enrollments = relationship(
        "Enrollment",
        back_populates="course",
        cascade="all, delete-orphan"
    )
    students = relationship(
        "Student",
        secondary="enrollments",
        viewonly=True
    )




class Enrollment(Base):
    __tablename__ = "enrollments"

    student_id = Column(Integer, ForeignKey("students.id"), primary_key=True)
    course_id = Column(String(30), ForeignKey("courses.id"), primary_key=True)
    grade = Column(Numeric(4,2))
    attended_sessions = Column(Integer)


    student = relationship("Student", back_populates="enrollments")
    course = relationship("Course", back_populates="enrollments")