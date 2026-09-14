from src.shared.helpers.external_interfaces.external_interface import IResponse, IRequest
from .update_user_usecase import UpdateUserUsecase
from .update_user_viewmodel import UpdateUserViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError
from pydantic import EmailStr, TypeAdapter, ValidationError


class UpdateUserController:

    def __init__(self, usecase: UpdateUserUsecase):
        self.UpdateUserUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:

        new_email = request.data.get('new_email')
        user_id = request.data.get('user_id')

        try:
            if user_id is None:
                raise MissingParameters('user_id')
            if new_email is None:
                raise MissingParameters('new_email')

            if type(user_id) != str:
                raise WrongTypeParameter(
                    fieldName="user_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=user_id.__class__.__name__
                )

            if type(new_email) != str:
                raise WrongTypeParameter(
                    fieldName="new_email",
                    fieldTypeExpected="str",
                    fieldTypeReceived=new_email.__class__.__name__
                )

            email_adapter = TypeAdapter(EmailStr)

            try: 
                email_adapter.validate_python(new_email)
            except ValidationError:
                raise WrongTypeParameter(
                    fieldName="new_email",
                    fieldTypeExpected="valid email",
                    fieldTypeReceived=new_email
                )

            user = self.UpdateUserUsecase(user_id=str(user_id), new_email=new_email)

            viewmodel = UpdateUserViewmodel(user=user)

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
