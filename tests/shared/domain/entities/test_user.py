import pytest
import uuid
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
from src.shared.helpers.errors.domain_errors import EntityError


class Test_User:
    def test_user_creation_success(self):
        user = User(
            id=uuid.UUID("2a32a42f-7b05-45c0-9a79-bbcb1c9ac875"),
            email="teste@teste.com",
            role=RoleEnum.USER,
            active=True,
            user_name="username_test"
        )
        assert user.id == uuid.UUID("2a32a42f-7b05-45c0-9a79-bbcb1c9ac875")
        assert user.email == "teste@teste.com"
        assert user.active == True
        assert user.user_name == "username_test"

    def test_user_invalid_email(self):
        with pytest.raises(EntityError):
            User(
                email="email_invalido",
                user_name="usuario_que_nao_coloca_email_valido"
            )

    def test_user_invalid_role(self):
        with pytest.raises(EntityError):
            User(
                email="teste@teste.com",
                role="ROLE_INVALIDA",
                user_name="usuario_que_nao_coloca_role_valida"
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
