from pydantic import BaseModel, EmailStr, field_validator


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    full_name: str

    @field_validator("password")
    @classmethod
    def validate_password_strength(cls, password: str) -> str:
        if len(password) < 8:
            raise ValueError("Password must be at least 8 characters long.")

        if not any(char.isupper() for char in password):
            raise ValueError("Password must contain at least one uppercase letter.")

        if not any(char.islower() for char in password):
            raise ValueError("Password must contain at least one lowercase letter.")

        if not any(char.isdigit() for char in password):
            raise ValueError("Password must contain at least one number.")

        special_characters = "!@#$%^&*()-_=+[]{};:,.<>?/|\\"

        if not any(char in special_characters for char in password):
            raise ValueError("Password must contain at least one special character.")

        return password


class RegisterResponse(BaseModel):
    message: str
    email: EmailStr
    full_name: str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    message: str
    email: EmailStr
    full_name: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class CurrentUserResponse(BaseModel):
    id: int
    email: EmailStr
    full_name: str
    role: str  
    is_active: bool