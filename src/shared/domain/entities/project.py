import uuid
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Project(BaseModel):
    MIN_TITLE_LENGTH = 3
    MIN_DESCRIPTION_LENGTH = 3

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        description="Id único do projeto"
    )

    title: str = Field(
        ...,
        description="Título do projeto"
    )

    description: str = Field(
        ...,
        description="Descrição do projeto"
    )

    associates: Optional[list[uuid.UUID]] = Field(
        default=None,
        description="Lista de ids dos usuários associados ao projeto"
    )

    display_image: Optional[str] = Field(
        default=None,
        description="URL ou path da imagem de exibição do projeto"
    )

    @staticmethod
    def validate_title(title: str) -> bool:
        if title is None:
            return False
        elif type(title) != str:
            return False
        elif len(title) < Project.MIN_TITLE_LENGTH:
            return False

        return True

    @staticmethod
    def validate_description(description: str) -> bool:
        if description is None:
            return False
        elif type(description) != str:
            return False
        elif len(description) < Project.MIN_DESCRIPTION_LENGTH:
            return False

        return True

    @field_validator("title")
    @classmethod
    def capitalize_title(cls, value: str) -> str:
        return value.capitalize()

    model_config = ConfigDict(
        use_enum_values=True,
        extra="forbid",
        populate_by_name=True,
    )