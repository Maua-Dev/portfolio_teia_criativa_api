from enum import Enum
from uuid import UUID, uuid4
import uuid
from pydantic import BaseModel, EmailStr, Field
from src.shared.domain.enums.role_enum import RoleEnum

class User(BaseModel):
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        description="Id unico do usuário"
    )
    email: EmailStr = Field(
        ...,
        description="Email do usuário"
    )
    role: RoleEnum = Field(
        default=RoleEnum.USER,
        description="Role do usuário"
    )
    senha_hash: str = Field(
        ...,
        description="Hash da senha do usuário"
    )

    class Config:
        frozen = True
