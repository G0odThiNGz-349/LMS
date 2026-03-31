from pydantic import BaseModel, EmailStr, ConfigDict, Field, field_validator
from datetime import date

class CourseCreate(BaseModel):
    code: str
    name: str
    description: str | None=None
    credits: int
    department_id: int

    model_config = ConfigDict(extra="forbid")


class CourseUpdate(BaseModel):
    code: str | None=None
    name: str | None=None
    description: str | None=None
    credits: int | None=None
    department_id: int | None=None

    model_config = ConfigDict(extra="forbid") 


class CourseResponse(BaseModel):
    code: str
    name: str
    description: str | None=None
    credits: int
    department_name: str

    model_config = ConfigDict(from_attributes=True)