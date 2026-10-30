from src.modules.member.delete_member.app.delete_member_usecase import DeleteMemberUsecase
from src.modules.member.delete_member.app.delete_member_viewmodel import DeleteMemberViewmodel
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import (
    BadRequest,
    Forbidden,
    InternalServerError,
    NotFound,
    OK,
)


class DeleteMemberController:
    def __init__(self, usecase: DeleteMemberUsecase):
        self.DeleteMemberUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            member_id = request.data.get("member_id")
            if member_id is None:
                raise MissingParameters("member_id")

            if not isinstance(member_id, str):
                raise WrongTypeParameter(
                    fieldName="member_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(member_id).__name__,
                )

            member = self.DeleteMemberUsecase(
                member_id=member_id,
                requester_id=self._get_requester_id(request),
            )
            return OK(DeleteMemberViewmodel(member).to_dict())

        except NoItemsFound as err:
            return NotFound(body=err.message)
        except ForbiddenAction as err:
            return Forbidden(body=err.message)
        except MissingParameters as err:
            return BadRequest(body=err.message)
        except WrongTypeParameter as err:
            return BadRequest(body=err.message)
        except EntityError as err:
            return BadRequest(body=err.message)
        except Exception as err:
            return InternalServerError(body=err)

    @staticmethod
    def _get_requester_id(request: IRequest) -> str | None:
        authorizer_user = request.data.get(USER_FROM_AUTHORIZER_KEY)
        if not isinstance(authorizer_user, dict):
            return None

        sub = authorizer_user.get("sub")
        return sub if isinstance(sub, str) else None
