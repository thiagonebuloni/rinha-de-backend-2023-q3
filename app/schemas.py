from pydantic import BaseModel
from datetime import date
from typing import Optional


class Pessoa(BaseModel):
    apelido: str
    nome: str
    nascimento: date
    stack: Optional[list[str]] = None

    def __getitem__(self, apelido: str) -> str:
        return apelido
