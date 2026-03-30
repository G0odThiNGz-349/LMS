from pydantic import BaseModel, Field ,ConfigDict
from datetime import date


class AcademicSemesterCreate(BaseModel):
    name: str
    start_date: date
    end_date: date
    is_current: bool= Field(default=True)

    model_config = ConfigDict(extra="forbid")


class AcademicSemesterUpdate(BaseModel):
    name: str | None=None
    start_date: date | None=None
    end_date: date | None=None
    is_current: bool | None=None

    model_config = ConfigDict(extra="forbid")


class AcademicSemesterResponse(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    is_current: bool

    model_config = ConfigDict(from_attributes=True)