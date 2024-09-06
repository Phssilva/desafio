from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from app.models.produtor import Produtor, Base_db
from app.config.database import SessionLocal, engine, Base
from app.schemas import ProdutorCreate, ProdutorRead
from faker import Faker


app = FastAPI()


print("Criando tabelas no banco de dados")
Base_db.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Rota para criar um novo produtor
@app.post("/produtores/", response_model=ProdutorRead)
def create_produtor(produtor: ProdutorCreate, db: Session = Depends(get_db)):
    db_produtor = (
        db.query(Produtor).filter(Produtor.cpf_cnpj == produtor.cpf_cnpj).first()
    )
    print(db_produtor)
    if db_produtor:
        raise HTTPException(status_code=400, detail="CPF ou CNPJ já cadastrado")

    if produtor.area_agricultavel + produtor.area_vegetacao > produtor.area_total:
        raise HTTPException(
            status_code=400,
            detail="A soma das áreas não pode ser maior que a área total",
        )

    new_produtor = Produtor(**produtor.dict())
    db.add(new_produtor)
    db.commit()
    db.refresh(new_produtor)
    return new_produtor


@app.post("/produtores/mock/")
def create_mock_produtores(qty: int = 10, db: Session = Depends(get_db)):
    fake = Faker("pt_BR")

    for _ in range(qty):
        produtor_data = ProdutorCreate(
            cpf_cnpj=fake.cpf(),
            nome_produtor=fake.name(),
            nome_fazenda=fake.company(),
            cidade=fake.city(),
            estado=fake.state_abbr(),
            area_total=fake.pyfloat(left_digits=4, right_digits=2, positive=True),
            area_agricultavel=fake.pyfloat(
                left_digits=3, right_digits=2, positive=True
            ),
            area_vegetacao=fake.pyfloat(left_digits=2, right_digits=2, positive=True),
            culturas_plantadas=fake.words(
                nb=3,
                ext_word_list=["Soja", "Milho", "Café", "Algodão", "Cana-de-Açúcar"],
            ),
        )

        while (
            produtor_data.area_agricultavel + produtor_data.area_vegetacao
            > produtor_data.area_total
        ):
            produtor_data.area_agricultavel = fake.pyfloat(
                left_digits=3, right_digits=2, positive=True
            )
            produtor_data.area_vegetacao = fake.pyfloat(
                left_digits=2, right_digits=2, positive=True
            )

        new_produtor = Produtor(**produtor_data.dict())
        db.add(new_produtor)

    db.commit()

    return {"detail": f"{qty} produtores fictícios criados com sucesso"}


# Rota para listar todos os produtores
@app.get("/produtores/", response_model=list[ProdutorRead])
def read_produtores(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    produtores = db.query(Produtor).offset(skip).limit(limit).all()
    return produtores


# Rota para obter um produtor pelo ID
@app.get("/produtores/{produtor_id}", response_model=ProdutorRead)
def read_produtor(produtor_id: int, db: Session = Depends(get_db)):
    produtor = db.query(Produtor).filter(Produtor.id == produtor_id).first()
    if not produtor:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")
    return produtor


# Rota para atualizar um produtor
@app.put("/produtores/{produtor_id}", response_model=ProdutorRead)
def update_produtor(
    produtor_id: int, produtor: ProdutorCreate, db: Session = Depends(get_db)
):
    db_produtor = db.query(Produtor).filter(Produtor.id == produtor_id).first()
    if not db_produtor:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")

    if produtor.area_agricultavel + produtor.area_vegetacao > produtor.area_total:
        raise HTTPException(
            status_code=400,
            detail="A soma das áreas não pode ser maior que a área total",
        )

    for key, value in produtor.dict().items():
        setattr(db_produtor, key, value)

    db.commit()
    db.refresh(db_produtor)
    return db_produtor


# Rota para deletar um produtor
@app.delete("/produtores/{produtor_id}")
def delete_produtor(produtor_id: int, db: Session = Depends(get_db)):
    db_produtor = db.query(Produtor).filter(Produtor.id == produtor_id).first()
    if not db_produtor:
        raise HTTPException(status_code=404, detail="Produtor não encontrado")

    db.delete(db_produtor)
    db.commit()
    return {"detail": "Produtor deletado com sucesso"}
