from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator, model_validator
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
    password:str = Field(min_length=8, max_length=128)

    model_config = ConfigDict(extra="forbid")


class UserResponse(UserBase):
    id: int
    last_login: datetime | None=None
    last_login_ip: str | None=None
    login_count: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class UserSelfUpdate(BaseModel):
    email: EmailStr | None=None
    password: str | None=None
    confirm_password: str | None= Field(default=None, exclude=True)

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password or self.confirm_password:
            if not self.password or not self.confirm_password:
                raise ValueError("Please confirm the password")
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self
    
    @field_validator("email")
    def lowercase_email(cls, v: str | None) -> str | None:
        if v:
            return v.lower()
        return v
    
    model_config = ConfigDict(extra="forbid")


class UserAdminUpdate(BaseModel):
    email: EmailStr | None=None
    role: UserRole | None=None
    is_active: bool | None=None
    password: str  | None=None

    @field_validator("password")
    def validate_password(cls, v):
        if v is None:
            return v
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        return v
    
    @field_validator("email")
    def lowercase_email(cls, v: str) -> str:
        if v:
            return v.lower()
        return v
    
    model_config = ConfigDict(extra="forbid")