from sqlalchemy import Column, Integer, String, ForeignKey, Numeric,Enum
from sqlalchemy.orm import relationship
from Database import Base
import enum

class UserRole(enum.Enum):
    student="student"
    professor = "professor"
    admin = "admin"

class login(Base):
    __tablename__="login"
    id= Column(String(15), unique=True, primary_key=True, nullable=False)
    email= Column(String(255), unique=True, nullable=False)
    password_hash= Column(String(225), nullable=False)
    role= Column(Enum(UserRole), nullable=False)