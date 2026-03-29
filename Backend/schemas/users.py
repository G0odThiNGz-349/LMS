from pydantic import BaseModel, EmailStr, ConfigDict
from enum import Enum
from datetime import datetime

class UserRole(str, Enum):
    student = "student"
    professor = "professor"
    teaching_assistant = "teaching_assistant"
    academic_affair = "academic_affair"
    it_staff = "it_staff"

class UserBase(BaseModel):
    university_id: str
    email: EmailStr | None=None
    role: UserRole
    is_active: bool = True

class UserCreate(UserBase):
    password:str

class UserResponse(UserBase):
    id: int
    last_login: datetime | None=None
    last_login_ip: str | None=None
    login_count: int
    created_at: datetime
    updated_at: datetime
    
    model_config= ConfigDict(from_attributes=True)


class UserSelfUpdate(BaseModel):
    email: EmailStr | None=None
    password: str | None=None

class UserAdminUpdate(BaseModel):
    email: EmailStr | None=None
    role: UserRole | None=None
    is_active: bool | None=None
    password: str | None=None