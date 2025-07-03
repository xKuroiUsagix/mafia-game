from datetime import datetime
from pydantic import BaseModel, EmailStr, model_validator


class UserCreateRequest(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str

    @model_validator(mode='after')
    def validate_passwords(self):
        if self.password != self.confirm_password:
            raise ValueError('Passwords do not match')
        if len(self.password) < 6:
            raise ValueError('Password must be at least 6 characters long')
        if not any(c.isalpha() for c in self.password):
            raise ValueError('Password must contain at least one letter')
        if not any(c.isdigit() for c in self.password):
            raise ValueError('Password must contain at least one number')
        return self


class UserResponse(BaseModel):
    id: int
    username: str
    email: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class ProfileCreateRequest(BaseModel):
    description: str | None = None


class ProfileResponse(BaseModel):
    id: int
    user_id: int
    description: str | None
    created_at: datetime
    updated_at: datetime
