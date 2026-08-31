#TEMP: arquivo desabilitado — fora do escopo desta branch / incompatível com contrato atual
from src.modules.update_user.app.update_user_viewmodel import UpdateUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum

import uuid

class Test_UpdateUserViewmodel:
    def test_update_user_viewmodel(self):
        user = User(
            id=uuid.UUID("af852f40-0135-406d-b5d7-7ed5dce9bc8e"),
            email="teste@test.com",
            role=RoleEnum.USER,
            senha_hash="hash_fake"
        )

        updated_user_viewmodel = UpdateUserViewmodel(user)

        expected = {
            'user_id': "af852f40-0135-406d-b5d7-7ed5dce9bc8e",
            'email': "teste@test.com",
            'role': RoleEnum.USER.value,
            'message': "the user was updated successfully"
        }

        assert expected == updated_user_viewmodel.to_dict()
