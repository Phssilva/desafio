from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = (
    "postgresql://brain_agriculture:123456@192.168.49.2:30007/brain-agriculture"
)

# Crie o engine
engine = create_engine(DATABASE_URL)

# Defina a base
Base = declarative_base()

# Defina sua classe de modelo (por exemplo, Produtor)
from sqlalchemy import Column, Integer, String, Float


class Produtor(Base):
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
        String, nullable=False
    )  # Pode ser um JSON ou lista separada por vírgulas


# Crie as tabelas no banco de dados
Base.metadata.create_all(bind=engine)
