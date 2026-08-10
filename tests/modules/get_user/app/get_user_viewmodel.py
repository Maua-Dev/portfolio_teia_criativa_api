from src.shared.domain.entities.user import User
from src.shared.domain.enums.role_enum import RoleEnum


class GetUserViewmodel:
    #user_id: str
    email: str
    role: RoleEnum

    def __init__(self, user: User):
        self.email = user.email
        self.role = user.role

    def to_dict(self):
        return {
            'email': self.email,
            'role': self.role.value,
            'message': "the user was retrieved successfully"
        }
