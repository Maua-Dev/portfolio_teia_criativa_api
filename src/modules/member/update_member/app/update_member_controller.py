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
from .update_member_usecase import UpdateMemberUsecase
from .update_member_viewmodel import UpdateMemberViewmodel


class UpdateMemberController:
    update_fields = ("new_member_photo", "new_member_name", "new_member_intro")

    def __init__(self, usecase: UpdateMemberUsecase):
        self.UpdateMemberUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        member_id = request.data.get("member_id")

        try:
            if member_id is None:
                raise MissingParameters("member_id")
            if type(member_id) is not str:
                raise WrongTypeParameter(
                    fieldName="member_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(member_id).__name__,
                )

            updates = {
                field: request.data.get(field)
                for field in self.update_fields
            }
            if all(value is None for value in updates.values()):
                raise MissingParameters(
                    "new_member_photo, new_member_name, or new_member_intro"
                )

            for field, value in updates.items():
                if value is not None and type(value) is not str:
                    raise WrongTypeParameter(
                        fieldName=field,
                        fieldTypeExpected="str",
                        fieldTypeReceived=type(value).__name__,
                    )

            member = self.UpdateMemberUsecase(member_id=member_id, **updates)
            viewmodel = UpdateMemberViewmodel(member)
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
