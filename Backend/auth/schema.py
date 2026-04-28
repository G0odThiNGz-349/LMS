from pydantic import BaseModel, EmailStr, ConfigDict


class RegisterRequest(BaseModel):
    university_id: str
    email: EmailStr | None=None
    password: str

    model_config = ConfigDict(extra="forbid")


class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenPayload(BaseModel):
    sub: str
    type: str