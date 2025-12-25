from pydantic import BaseModel

class PodeCursarRequest(BaseModel):
    aluno_id: int
    materia: str

class PodeCursarAlunoRequest(BaseModel):
    materia: str

class LoginRequest(BaseModel):
    dadoLogin: str
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

class MateriaFazendo(BaseModel):
    id_materia: int

class AdicionarComentario(BaseModel):
    id_materia: int
    comentario: str
    
class AtualizarComentario(BaseModel):
    id_comentario: int
    novo_comentario: str
    
class DeletarComentario(BaseModel):
    id_comentario: int
    
class AdicionarNota(BaseModel):
    id_materia: int
    nota: int
    
class AtualizarNota(BaseModel):
    id_nota: int
    nova_nota: int
    
class RemoverNota(BaseModel):
    id_nota: int
    
class AdicionarDificuldade(BaseModel):
    id_materia: int
    dificuldade: int
    
class AtualizarDificuldade(BaseModel):
    id_dificuldade: int
    nova_dificuldade: int

class RemoverDificuldade(BaseModel):
    id_dificuldade: int