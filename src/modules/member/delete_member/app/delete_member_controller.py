from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import (
    OK,
    NotFound,
    BadRequest,
    InternalServerError,
)
from .delete_member_usecase import DeleteMemberUsecase
from .delete_member_viewmodel import DeleteMemberViewmodel


class DeleteMemberController:
    def __init__(self, usecase: DeleteMemberUsecase):
        self.DeleteMemberUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        member_id = request.data.get("member_id")

        try:
            if member_id is None:
                raise MissingParameters("member_id")

            if not isinstance(member_id, str):
                raise WrongTypeParameter(
                    fieldName="member_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(member_id).__name__,
                )

            member = self.DeleteMemberUsecase(member_id=member_id)
            viewmodel = DeleteMemberViewmodel(member)
            return OK(viewmodel.to_dict())

        except NoItemsFound as err:
            return NotFound(body=err.message)
        except MissingParameters as err:
            return BadRequest(body=err.message)
        except WrongTypeParameter as err:
            return BadRequest(body=err.message)
        except EntityError as err:
            return BadRequest(body=err.message)
        except Exception as err:
            return InternalServerError(body=str(err))
