from pydantic import BaseModel, ConfigDict
from datetime import date

class CourseofferingCreate(BaseModel):
    course_id: int
    semester_id: int
    professor_user_id: int
    start_date: date
    end_date: date

    model_config = ConfigDict(extra="forbid")


class CourseofferingUpdate(BaseModel):
    course_id: int | None=None
    semester_id: int | None=None
    professor_user_id: int | None=None
    start_date: date | None=None
    end_date: date | None=None

    model_config = ConfigDict(extra="forbid")


class CourseofferingResponse(BaseModel):
    course_id: int 
    semester_id: int
    professor_user_id: int
    start_date: date
    end_date: date

    model_config = ConfigDict(from_attributes=True)
