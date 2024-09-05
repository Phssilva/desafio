from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Carregando variáveis de ambiente para proteger informações sensíveis
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://brain_agriculture:123456@postgres_container:5432/brain-agriculture",
)

# Criando o engine do SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Criando a fábrica de sessões
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarando a base para os modelos
Base = declarative_base()
