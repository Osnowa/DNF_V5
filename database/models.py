from beanie import Document
from pydantic import Field


class User(Document):
    '''Описываем документ (строка) в БД'''
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)
    notes: list[str] = Field(default_factory=list, max_length=5) # заметки, все в 1 таблице

    class Settings:
        name = "users" # название коллекции