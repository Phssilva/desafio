from pydantic import BaseModel
from typing import List


class ProdutorBase(BaseModel):
    cpf_cnpj: str
    nome_produtor: str
    nome_fazenda: str
    cidade: str
    estado: str
    area_total: float
    area_agricultavel: float
    area_vegetacao: float
    culturas_plantadas: List[str]


class ProdutorCreate(BaseModel):
    cpf_cnpj: str
    nome_produtor: str
    nome_fazenda: str
    cidade: str
    estado: str
    area_total: float
    area_agricultavel: float
    area_vegetacao: float
    culturas_plantadas: List[str]


class ProdutorRead(ProdutorBase):
    id: int

    class Config:
        orm_mode = True
