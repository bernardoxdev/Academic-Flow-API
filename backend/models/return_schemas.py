from pydantic import BaseModel
from typing import List, Dict

class PreRequisito(BaseModel):
    id: str
    nome: str

class FluxogramaReturn(BaseModel):
    id: str
    nome: str
    semestre: int
    pre_requisitos: List[PreRequisito]
    
class PreRequesitoCompleto(BaseModel):
    codigo: str
    nome: str
    semestre: int
    
class RequesitosCompletos(BaseModel):
    materia: str
    quantidade: int
    pre_requesitos: List[PreRequesitoCompleto]
    
class Progresso(BaseModel):
    aluno_id: int
    materias_concluidas: List[str]
    quantidade: int
    
class Status(BaseModel):
    status: str
    
class LoginAndRegister(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    
class Refresh(BaseModel):
    access_token: str
    token_type: str
    
class Materias(BaseModel):
    id: str
    nome: str
    
class MateriasFazendo(BaseModel):
    materias: List[str]
    
class Comentario(BaseModel):
    id_materia: str
    
class Comentarios(BaseModel):
    comentarios: Dict[Comentario]
    
class Dificuldade(BaseModel):
    id_materia: int
    
class Dificuldades(BaseModel):
    dificuldades: Dict[Dificuldade]

class Nota(BaseModel):
    id_materia: int
    
class Notas(BaseModel): 
    notas: Dict[Nota]
    
class MateriasFaltando(BaseModel):
    materias: List[str]
    
class Aluno(BaseModel):
    id: int
    username: str
    email: str
    matricula: str
    hashed_password: str
    role: str
    
class Alunos(BaseModel):
    alunos: List[Aluno]

class PodeCursarItem(BaseModel):
    aluno_id: int
    materia: str
    pode_cursar: bool

class PodeCursar(BaseModel):
    pode_cursar: List[PodeCursarItem]