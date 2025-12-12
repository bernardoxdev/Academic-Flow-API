from pydantic import BaseModel

class PodeCursarRequest(BaseModel):
    aluno_id: int
    materia: str

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

class ChangePasswordRequest(BaseModel):
    new_password: str