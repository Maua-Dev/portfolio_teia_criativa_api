from src.modules.microsoft_authorizer.app.microsoft_authorizer_usecase import MicrosoftAuthorizerUsecase
from src.modules.microsoft_authorizer.app.microsoft_authorizer_viewmodel import MicrosoftAuthorizerViewmodel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, InternalServerError, NotFound
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS

from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
from .microsoft_authorizer_usecase import MicrosoftAuthorizerUsecase
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoUsersFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, BadRequest, InternalServerError
from aws_lambda_powertools import Logger


class MicrosoftAuthorizerController:

    def __init__(self, usecase: MicrosoftAuthorizerUsecase, observability: ObservabilityAWS):
        self.MicrosoftAuthorizerUsecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        try:
            self.observability.log_controller_in()

            authorization_token = request.data.get('authorization_token')
            method_arn = request.data.get('method_arn')

            if authorization_token is None:
                raise MissingParameters('authorization_token')

            if method_arn is None:
                raise MissingParameters('method_arn')

            if type(authorization_token) != str:
                raise WrongTypeParameter(
                    fieldName="authorization_token",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('authorization_token').__class__.__name__
                )

            if type(method_arn) != str:
                raise WrongTypeParameter(
                    fieldName="method_arn",
                    fieldTypeExpected="str",
                    fieldTypeReceived=request.data.get('method_arn').__class__.__name__
                )

            result = self.MicrosoftAuthorizerUsecase(
                authorization_token=authorization_token,
                method_arn=method_arn
            )

            viewmodel = MicrosoftAuthorizerViewmodel(was_created=result.was_created)

            response = OK(viewmodel.to_dict)
            self.observability.log_controller_out(input=result.policy.get('principalId'))
            return response

        except MissingParameters as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except EntityError as err:
            self.observability.log_exception(message=err.message)
            return BadRequest(body=err.message)

        except Exception as err:
            self.observability.log_exception(message=err.args[0])
            return InternalServerError(body=err.args[0])