from pydantic import BaseModel

class PodeCursarRequest(BaseModel):
    aluno_id: int
    materia: str

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    email: str
    matricula: str
    password: str
    
class RegisterAdminRequest(BaseModel):
    username: str
    email: str
    matricula: str
    password: str
    role: str

class ChangePasswordRequest(BaseModel):
    new_password: str