from beanie import PydanticObjectId
from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    surname: str = Field(..., min_length=1, max_length=100)
    age: int = Field(..., ge=0, le=150)
    notes: list[str] = Field(default_factory=list, max_length=5)

class UserUpdate(BaseModel):
    name: str | None = Field(None, min_length=1, max_length=100)
    surname: str | None = Field(None, min_length=1, max_length=100)
    age: int | None = Field(None, ge=0, le=150)
    notes: list[str] | None = Field(None, max_length=5)
    
class UserResponse(BaseModel):
    id: PydanticObjectId
    first_name: str
    last_name: str
    age: int
    notes: list[str]