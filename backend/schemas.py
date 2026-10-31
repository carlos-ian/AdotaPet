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

class PetSchema(BaseModel):
    nome: str
    especie: str
    raca: Optional[str] = None
    idade: Optional[int] = None
    porte: Optional[str] = None
    sexo: Optional[str] = None
    status: str
    observacao: Optional[str] = None
    id_instituicao: int

class StatusAdocaoSchema(BaseModel):
    id_adotante: int
    id_animal: int
    status: str
    observacao: Optional[str] = None

class StatusApadrinhamentoSchema(BaseModel):
    id_adotante: int
    id_animal: int
    status: str

class ProntuarioSchema(BaseModel):
    id_animal: int
    tipo_procedimento: str
    descricao: Optional[str] = None
    data_procedimento: Optional[str] = None

class InstituicaoUpdateSchema(BaseModel):
    razao_social: str
    cnpj: str
    email: EmailStr
    rua: Optional[str] = None
    numero: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    estado: Optional[str] = None
    cep: Optional[str] = None
    complemento: Optional[str] = None
    telefones: List[str] = []
