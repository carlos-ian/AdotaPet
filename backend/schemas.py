# backend/schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional, List

# Schema para o corpo do JSON Usuário (Login)
class LoginSchema(BaseModel):
    email: EmailStr
    senha: str
    tipo_usuario: str

# Schema para o corpo do JSON de Usuário
class RegistroSchema(BaseModel):
    email: EmailStr
    senha: str
    tipo_usuario: str
    rua: Optional[str] = None
    numero: Optional[str] = None
    bairro: Optional[str] = None
    cep: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    complemento: Optional[str] = None
    telefones: List[str] = []
    
    nome: Optional[str] = None
    cpf: Optional[str] = None
    tipo_residencia: Optional[str] = None
    historico_pets: Optional[str] = None
    
    razao_social: Optional[str] = None
    cnpj: Optional[str] = None