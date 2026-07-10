from enum import Enum
from uuid import UUID, uuid4
from pydantic import BaseModel, EmailStr, Field

class RoleEnum(str, Enum):
    ADMIN = "Admin"
    USER = "User"

class User(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    role: RoleEnum
    senha_hash: str

    class Config:
        frozen = True
