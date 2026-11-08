from src.shared.helpers.errors.external_errors import JwtVerificationError
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
from .login_usecase import LoginUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound, InvalidJwtFormat, EnvVarNotFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError
from .login_viewmodel import LoginViewmodel


class LoginController:

    def __init__(self, usecase: LoginUsecase, observability: ObservabilityAWS):
        self.usecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        
        try:
            id_token = request.data.get("id_token")

            if id_token is None:
                raise MissingParameters("id_token")
            if not isinstance(id_token, str):
                raise WrongTypeParameter(
                    fieldName="id_token",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(id_token).__name__,
                )

            access_token, refresh_token, user_info = self.usecase(
                id_token=id_token
            )

            viewmodel = LoginViewmodel(access_token=access_token, user=user_info)
            return OK(
                body=viewmodel.to_dict(),
                headers={
                    "Set-Cookie": (
                        f"refresh_token={refresh_token}; HttpOnly; Secure; "
                        "SameSite=Strict; Path=/; Max-Age=604800"
                    )
                },
            )
            
        except JwtVerificationError as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)
            
        except NoItemsFound as err:
            self.observability.log_exception(message=err.message)
            return NotFound(body=err.message)

        except MissingParameters as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except EntityError as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except InvalidJwtFormat as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except EnvVarNotFound as err:
            self.observability.log_exception(message=err.message)
            return InternalServerError(body=err.message)

        except Exception as err:
            self.observability.log_exception(message=err.args[0])
            return InternalServerError(body=err.args[0])
