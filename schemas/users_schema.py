from pydantic import BaseModel, EmailStr, Field, model_validator

class UserCreate(BaseModel):
    fullname: str
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)
    confirm_password: str

    @model_validator(mode="after")
    def check_passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Password and Confirm Password must be same")
        return self
    

class LoginRequest(BaseModel):
    email: EmailStr
    password: str