from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class DeleteUserViewmodel:
    user_id: str
    email: str
    role: RoleEnum

    def __init__(self, user: User):
        self.user_id = user.id
        self.email = user.email
        self.role = user.role

    def to_dict(self):
        return {
            'user_id': str(self.user_id),
            'email': self.email,
            'role': self.role.value,
            'message': "the user was deleted successfully"
        }
