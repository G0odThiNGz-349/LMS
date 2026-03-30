from pydantic import BaseModel, ConfigDict

class CoursePrerequisitesResponse(BaseModel):
    course_code: str
    prerequisite_course_code: str
    course_name: str
    prerequisite_course_name: str

    model_config = ConfigDict(from_attributes=True)

class CoursePrerequisitesCreate(BaseModel):
    course_id: int
    prerequisite_course_id: int | None=None

    model_config = ConfigDict(extra="forbid")


class CoursePrerequisitesUpdate(BaseModel):
    course_id: int | None=None
    prerequisite_course_id: int | None=None

    model_config = ConfigDict(extra="forbid")

