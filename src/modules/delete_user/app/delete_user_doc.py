from pydantic import BaseModel, Field

from src.shared.helpers.openapi.route_doc import ApiRouteDoc


class DeleteUserRequest(BaseModel):
    user_id: str = Field(
        ...,
        description="UUID do usuário a deletar",
        examples=["af852f40-0135-406d-b5d7-7ed5dce9bc8e"],
    )


class DeleteUserResponse(BaseModel):
    user_id: str = Field(..., description="UUID do usuário deletado")
    email: str = Field(..., description="Email do usuário deletado")
    role: str = Field(..., description="Role do usuário (Admin | User)")
    message: str = Field(
        ...,
        description="Mensagem de confirmação",
        examples=["the user was deleted successfully"],
    )


DOC = ApiRouteDoc(
    method="DELETE",
    path="/delete-user",
    summary="Deleta um usuário",
    description="Remove o usuário pelo user_id (UUID em string).",
    tags=["users"],
    request_model=DeleteUserRequest,
    response_model=DeleteUserResponse,
)
