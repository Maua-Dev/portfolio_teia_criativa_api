from src.modules.user.create_user.app.create_user_viewmodel import CreateUserViewmodel
from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class Test_CreateUserViewModel:
    def test_create_user_viewmodel(self):
        user = User(
            email="teste@teste.com",
            role=RoleEnum.USER,
            senha_hash="hash_seguro",
        )
        viewmodel = CreateUserViewmodel(user)

        response = viewmodel.to_dict()

        assert response == {
            'id': str(user.id),
            'email': 'teste@teste.com',
            'role': RoleEnum.USER.value,
            'message': 'the user was created successfully'
        }
