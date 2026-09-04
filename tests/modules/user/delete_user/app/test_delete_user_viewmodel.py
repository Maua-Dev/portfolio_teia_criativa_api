from src.modules.user.delete_user.app.delete_user_viewmodel import DeleteUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum
import uuid

class Test_DeleteUserViewmodel:
    def test_delete_user_viewmodel(self):

        user_id = str(uuid.uuid4())

        user = User(
            id= user_id,
            name="Vitinho da Silva",
            email="21.01444-2@maua.br",
            role=RoleEnum.USER,
            senha_hash='hash_fake')

        delete_user_viewmodel = DeleteUserViewmodel(user)

        expected = {
                    'user_id': user_id,
                    'email': '21.01444-2@maua.br',
                    'role': 'User',
                    'message': 'the user was deleted successfully'}

        assert expected == delete_user_viewmodel.to_dict()
