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

#from src.shared.domain.entities.user import User
#from src.shared.domain.enums.state_enum import STATE
#from src.shared.helpers.errors.domain_errors import EntityError
#import pytest


#class Test_User:
#    def test_user(self):
#        User(name="VITOR", email="21.01444-2@maua.br", user_id=1, state=STATE.APPROVED)

#    def test_user_name_is_none(self):
#       with pytest.raises(EntityError):
#           User(name=None, email="21.01444-2@maua.br", user_id=1, state=STATE.APPROVED)

#   def test_user_name_is_not_str(self):
#       with pytest.raises(EntityError):
#           User(name=1, email="21.01444-2@maua.br", user_id=1, state=STATE.APPROVED)

#   def test_user_name_is_shorter_than_min_length(self):
#       with pytest.raises(EntityError):
#           User(name="V", email="21.01444-2@maua.br", user_id=1, state=STATE.APPROVED)

#   def test_user_email_is_none(self):
#       with pytest.raises(EntityError):
#           User(name="VITOR", email=None, user_id=1, state=STATE.APPROVED)

#   def test_user_email_is_not_valid(self):
#       with pytest.raises(EntityError):
#           User(name="VITOR", email="21.01444-2maua.br", user_id=1, state=STATE.APPROVED)

#   def test_user_user_id_is_not_int(self):
#       with pytest.raises(EntityError):
#           User(name="VITOR", email="21.01444-2@maua.br", user_id="1", state=STATE.APPROVED)

#   def test_user_user_id_is_negative(self):
#       with pytest.raises(EntityError):
#           User(name="VITOR", email="21.01444-2@maua.br", user_id=-1, state=STATE.APPROVED)

#   def test_user_state_is_not_sate_enum(self):
#       with pytest.raises(EntityError):
#           User(name="VITOR", email="21.01444-2@maua.br", user_id=1, state="APPROVED")
