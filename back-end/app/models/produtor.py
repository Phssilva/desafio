from sqlalchemy import Column, String, Integer, Float, JSON
from sqlalchemy.orm import declarative_base


Base_db = declarative_base()


class Produtor(Base_db):
    __tablename__ = "produtores"

    id = Column(Integer, primary_key=True, autoincrement=True)
    cpf_cnpj = Column(String(18), unique=True, nullable=False)
    nome_produtor = Column(String(100), nullable=False)
    nome_fazenda = Column(String(100), nullable=False)
    cidade = Column(String(100), nullable=False)
    estado = Column(String(2), nullable=False)  # UF: Exemplo "SC", "SP"
    area_total = Column(Float, nullable=False)  # Área total em hectares
    area_agricultavel = Column(Float, nullable=False)  # Área agricultável em hectares
    area_vegetacao = Column(Float, nullable=False)  # Área de vegetação em hectares
    culturas_plantadas = Column(
        JSON, nullable=False
    )  # Usando JSON para armazenar a lista de culturas

    def __repr__(self):
        return f"<Produtor(id={self.id}, nome_produtor='{self.nome_produtor}', nome_fazenda='{self.nome_fazenda}')>"
