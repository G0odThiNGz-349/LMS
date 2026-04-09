from pydantic import BaseModel, ConfigDict

class CoursePrerequisitesResponse(BaseModel):
    course_code: str
    prerequisite_course_code: str | None=None
    course_name: str
    prerequisite_course_name: str | None=None

    model_config = ConfigDict(from_attributes=True)

class CoursePrerequisitesCreate(BaseModel):
    course_name: str
    prerequisite_course_name: str | None=None

    model_config = ConfigDict(extra="forbid")


class CoursePrerequisitesUpdate(BaseModel):
    course_name: str | None=None
    prerequisite_course_name: str | None=None

    model_config = ConfigDict(extra="forbid")

