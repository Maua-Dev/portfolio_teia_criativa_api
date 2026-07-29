from enum import Enum
from uuid import UUID, uuid4
import uuid
from pydantic import BaseModel, EmailStr, Field, ValidationError
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.domain_errors import EntityError



class User(BaseModel):
    
    def __init__(self, **data):
        try:
            super().__init__(**data)
        except ValidationError as err:
            raise EntityError(str(err.errors()[0]["loc"][0])) from err
 
    
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
