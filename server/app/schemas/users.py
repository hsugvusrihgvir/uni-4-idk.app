from pydantic import BaseModel, ConfigDict, EmailStr, constr


# GET /api/v1/users/check-username
class UsernameCheckResponse(BaseModel):
    available: bool
    message: str


# GET /api/v1/users/me
class UserMeResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    username: str
    name: str | None
    photo_url: str | None


# PATCH /api/v1/users/me
class UserMeUpdateRequest(BaseModel):
    username: constr(max_length=50, min_length=3) | None = None
    name: constr(max_length=255) | None = None
    photo_url: constr(max_length=500) | None = None
