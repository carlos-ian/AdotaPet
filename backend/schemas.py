from pydantic import BaseModel, EmailStr
from typing import Optional, List

class LoginSchema(BaseModel):
    email: EmailStr
    senha: str
    tipo_usuario: str

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

class AdocaoSchema(BaseModel):
    id_adotante: int
    id_animal: int
    observacao: Optional[str] = None

class ApadrinhamentoSchema(BaseModel):
    id_adotante: int
    id_animal: int
    tipo_de_contribuicao: str
    valor_recorrente: float
    frequencia: str
