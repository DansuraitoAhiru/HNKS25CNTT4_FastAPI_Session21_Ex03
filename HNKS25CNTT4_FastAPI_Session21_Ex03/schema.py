from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: str


class RegisterResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    is_active: bool


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str
    is_active: bool