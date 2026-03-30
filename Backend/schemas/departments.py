from pydantic import BaseModel, ConfigDict

class DepartmentCreate(BaseModel):
    name: str
    head_prof_university_id: str | None = None

    model_config = ConfigDict(extra="forbid")

class DepartmentUpdate(BaseModel):
    name: str | None=None
    head_prof_university_id: str | None = None

class UserMini(BaseModel):
    id: int
    university_id: str
    ful_name: str

    model_config = ConfigDict(from_attributes=True)

class DepartmentDetailedResponse(BaseModel):
    id: int
    name: str
    head_professor: UserMini | None = None

    model_config = ConfigDict(from_attributes=True)
