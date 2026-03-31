from pydantic import BaseModel, ConfigDict


class ResouceCreate(BaseModel):
    course_offering_id: int
    title: str
    file_url: str
    resource_type: str

    model_config = ConfigDict(extra="forbid")


class ResourceUpdate(BaseModel):
    course_offering_id: int | None=None
    title: str | None=None
    file_url: str | None=None
    resource_type: str | None=None

    model_config = ConfigDict(extra="forbid")


class ResourceResponse(BaseModel):
    title: str
    file_url: str
    resource_type: str

    model_config = ConfigDict(from_attributes=True)

    