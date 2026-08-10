from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from .delete_user_usecase import DeleteUserUsecase
from .delete_user_viewmodel import DeleteUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError

import uuid


class DeleteUserController:

    def __init__(self, usecase: DeleteUserUsecase):
        self.DeleteUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:

        user_id = request.data.get('user_id')

        try:
            if user_id is None:
                raise MissingParameters('user_id')

            if not isinstance(user_id,str):
                raise WrongTypeParameter(
                    fieldName="user_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=user_id.__class__.__name__
                )

            try:
                uuid.UUID(user_id)
            except ValueError:
                raise EntityError("user_id")

            user = self.DeleteUserUsecase(
                user_id=str(user_id)
            )

            viewmodel = DeleteUserViewmodel(user=user)

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

            return InternalServerError(body=err.args[0])
