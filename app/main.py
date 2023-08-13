from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy import or_
from sqlalchemy.orm import Session
import uuid
from . import models, schemas
from .database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/", tags=["get"])
async def root():
    return {"message": "Hello world"}


@app.post(
    "/pessoas",
    tags=["post"],
    status_code=status.HTTP_201_CREATED,
)
async def pessoas(
    nova_pessoa: schemas.Pessoa, db: Session = Depends(get_db)
) -> schemas.Pessoa:
    try:
        pessoa_ja_existe = (
            db.query(models.Pessoa)
            .filter(models.Pessoa.apelido == nova_pessoa.apelido)
            .first()
        )
    except Exception:
        print("pessoa ja existe")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unprocessable Entity.",
        )

    if pessoa_ja_existe:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unprocessable Entity",
        )

    try:
        pessoa = models.Pessoa(id=uuid.uuid4(), **nova_pessoa.model_dump())
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Unprocessable Entity.",
        )

    db.add(pessoa)
    db.commit()
    db.refresh(pessoa)

    return pessoa


@app.get("/pessoas/{id}", tags=["get"])
async def get_pessoas(id: str, db: Session = Depends(get_db)) -> schemas.Pessoa:
    try:
        pessoa = db.query(models.Pessoa).filter(models.Pessoa.id == id).first()
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    return pessoa


@app.get("/pessoas_busca/{term}", tags=["get"])
async def pessoas_busca(term: str, db: Session = Depends(get_db)):
    pessoa = db.query(models.Pessoa).filter(models.Pessoa.stack.in_([{term}])).all()
    if not pessoa:
        term = f"%{term}%"
        pessoa = (
            db.query(models.Pessoa)
            .filter(
                or_(models.Pessoa.apelido.ilike(term), models.Pessoa.nome.ilike(term))
            )
            .all()
        )

    return pessoa if pessoa else []


@app.get("/contagem_pessoas", tags=["get"])
async def pessoas_count(db: Session = Depends(get_db)) -> int:
    contagem = db.query(models.Pessoa).count()
    return contagem
