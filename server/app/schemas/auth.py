from pydantic import BaseModel, ConfigDict, EmailStr, constr


# POST /api/v1/auth/login
class AuthLoginRequest(BaseModel):
    email: EmailStr


class AuthLoginResponse(BaseModel):
    exists: bool
    message: constr(max_length=200)


# POST /api/v1/auth/register
class AuthRegisterRequest(BaseModel):
    email: EmailStr
    username: constr(max_length=50, min_length=3)
    name: constr(max_length=255) | None = None
    photo_url: constr(max_length=500) | None = None


class AuthMessageResponse(BaseModel):
    message: constr(max_length=200)


# POST /api/v1/auth/verify
class AuthVerifyRequest(BaseModel):
    email: EmailStr
    code: constr(max_length=10, min_length=4)


class AuthUserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    email: EmailStr
    username: str
    name: str | None
    photo_url: str | None


class AuthVerifyResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: AuthUserResponse


# POST /api/v1/auth/refresh
class AuthRefreshRequest(BaseModel):
    refresh_token: str


class AuthRefreshResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
