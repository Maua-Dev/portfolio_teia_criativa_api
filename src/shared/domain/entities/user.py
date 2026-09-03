import uuid
from pydantic import BaseModel, ConfigDict, EmailStr, Field, ValidationError
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.domain_errors import EntityError


class User(BaseModel):
    model_config = ConfigDict(frozen=True)
    # Frozen vai travar essa entidade, mas temos campos que provavelmente poderão ser alterados
    # Ex: active, user_name. Acho que vale remover

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
    active: bool = Field(
        default=True,
        description="Usuário Ativo"
    )
    user_name: str =  Field(
        ...,
        description="Nome do usuário"
    )