from pydantic import BaseModel, EmailStr

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class LoginResponse(BaseModel):
    message: str
    user_id: int
    email: str
    access_token: str
    token_type: str
    role: str