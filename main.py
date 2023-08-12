from datetime import date
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from unidecode import unidecode
import uuid

app = FastAPI()

my_people = [
    {
        "id": uuid.uuid4(),
        "apelido": "josé",
        "nome": "josé roberto",
        "nascimento": "1986-10-01",
        "stack": ["Python", "C#", "PostgreSQL"],
    },
    {
        "id": uuid.uuid4(),
        "apelido": "rodrigo",
        "nome": "rodrigo falcao",
        "nascimento": "1980-01-10",
        "stack": ["Scala", "TypeScript", "SQL Server"],
    },
    {
        "id": uuid.uuid4(),
        "apelido": "josé",
        "nome": "josé rodrigo",
        "nascimento": "1986-10-01",
        "stack": ["Python", "Scala", "MySQL"],
    },
]


class Pessoa(BaseModel):
    apelido: str
    nome: str
    nascimento: date
    stack: Optional[list[str]] = None

    def __getitem__(self, apelido):
        return apelido


def find_people(id: int) -> dict | None:
    for p in my_people:
        if p["id"] == id:
            return p


def find_term(term: str) -> list | None:
    result = []
    for p in my_people:
        if (
            term in unidecode(p["apelido"]).lower()
            or term in unidecode(p["nome"]).lower()
        ):
            result.append(p)
            continue
        for s in p["stack"]:
            if term in unidecode(s).lower():
                result.append(p)
    return result


@app.get("/")
async def root():
    return {"message": "Hello world"}


@app.post("/pessoa")
async def pessoas(new_pessoa: Pessoa, response: Response):
    pessoa_ja_existente = find_term(unidecode(new_pessoa.apelido).lower())

    if pessoa_ja_existente:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Já adastrado"
        )

    response.status_code = status.HTTP_201_CREATED
    return new_pessoa


@app.get("/pessoa_id/{id}")
async def get_pessoas(id: int):
    people = find_people(id)
    if not people:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return {"data": people}


@app.get("/pessoas/{term}")
async def pessoas_search(term: str):
    people = find_term(unidecode(term).lower())
    return people if people else []


@app.get("/pessoa_contagem")
async def pessoas_count():
    return len(my_people)
