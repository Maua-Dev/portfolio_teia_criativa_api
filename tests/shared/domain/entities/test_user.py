import pytest
from uuid import uuid4
from pydantic import ValidationError
from src.shared.domain.entities.user import User, RoleEnum

class Test_User:
    def test_user_creation_success(self):
        """Sucesso ao criar usuário com dados válidos"""
        user_id = uuid4()
        user = User(
            id=user_id,
            email="vitor@maua.br",
            role=RoleEnum.USER,
            senha_hash="senha_secreta_123"
        )
        assert user.id == user_id
        assert user.email == "vitor@maua.br"
        assert user.role == RoleEnum.USER

    def test_user_invalid_email(self):
        """Pydantic deve barrar e-mail inválido"""
        with pytest.raises(ValidationError):
            User(
                email="vitor.maua.br",  # Sem o @
                role=RoleEnum.USER,
                senha_hash="123456"
            )

    def test_user_invalid_role(self):
        """Pydantic deve barrar role que não existe no Enum"""
        with pytest.raises(ValidationError):
            User(
                email="vitor@maua.br",
                role="INVALID_ROLE",
                senha_hash="123456"
            )
