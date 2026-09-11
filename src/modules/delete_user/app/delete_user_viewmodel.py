from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class DeleteUserViewmodel:
    user_id: str
    email: str
    role: RoleEnum
    active: bool
    user_name: str

    def __init__(self, user: User):
        self.user_id = user.id
        self.email = user.email
        self.role = user.role
        self.active = user.active
        self.user_name = user.user_name

    def to_dict(self):
        return {
            'user_id': str(self.user_id),
            'email': self.email,
            'role': self.role.value,
            'active': self.active,
            'user_name': self.user_name,
            'message': "the user was deleted successfully"
        }
