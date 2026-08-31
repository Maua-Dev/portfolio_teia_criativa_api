from dataclasses import dataclass, field
from typing import Optional, Type

from pydantic import BaseModel, Field


class ErrorResponse(BaseModel):
    """Resposta padrão de erro das rotas (body string no HTTP codes atuais)."""

    message: str = Field(
        ...,
        description="Mensagem de erro retornada pela API",
        examples=["Field user_id is missing"],
    )


@dataclass(frozen=True)
class ApiRouteDoc:
    """
    Contrato do arquivo único por rota (`*_doc.py`).

    O trainee só precisa exportar `DOC = ApiRouteDoc(...)` no módulo.
    """

    method: str
    path: str
    summary: str
    description: str = ""
    tags: list[str] = field(default_factory=list)
    request_model: Optional[Type[BaseModel]] = None
    response_model: Optional[Type[BaseModel]] = None
    error_statuses: tuple[int, ...] = (400, 404, 500)
    error_model: Type[BaseModel] = ErrorResponse
