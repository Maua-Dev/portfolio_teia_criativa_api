from uuid import UUID

from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .create_user_usecase import CreateUserUsecase
from .create_user_viewmodel import CreateUserViewmodel
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import NotFound, BadRequest, Created, Forbidden, InternalServerError


class CreateUserController:
    def __init__(self, usecase: CreateUserUsecase):
        self.CreateUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            email = request.data.get('email', None)
            user_name = request.data.get('user_name', None)

            if email is None:
                raise MissingParameters('email')
            if type(email) != str:
                raise WrongTypeParameter(fieldName='email', fieldTypeExpected=str, fieldTypeReceived=type(email))

            if user_name is None:
                raise MissingParameters('user_name')
            if type(user_name) != str:
                raise WrongTypeParameter(fieldName='user_name', fieldTypeExpected=str, fieldTypeReceived=type(user_name))

            user_from_authorizer = request.data.get(USER_FROM_AUTHORIZER_KEY)
            if user_from_authorizer is None:
                raise MissingParameters(USER_FROM_AUTHORIZER_KEY)

            requester_user_id = user_from_authorizer.get("sub")
            if requester_user_id is None:
                raise MissingParameters("sub")
            if not isinstance(requester_user_id, str):
                raise WrongTypeParameter(
                    fieldName="sub",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(requester_user_id).__name__
                )

            try:
                parsed_requester_user_id = UUID(requester_user_id)
            except ValueError:
                raise EntityError("user_id")

            user = self.CreateUserUsecase(
                email=email,
                user_name=user_name,
                requester_user_id=parsed_requester_user_id,
            )

            viewmodel = CreateUserViewmodel(user)

            return Created(viewmodel.to_dict())

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
            return InternalServerError(body=err.args[0])
