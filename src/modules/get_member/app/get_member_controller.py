from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import OK, NotFound, BadRequest, InternalServerError
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS
from .get_member_usecase import GetMemberUsecase
from .get_member_viewmodel import GetMemberViewmodel


class GetMemberController:
    def __init__(self, usecase: GetMemberUsecase, observability: ObservabilityAWS):
        self.GetMemberUsecase = usecase
        self.observability = observability

    def __call__(self, request: IRequest) -> IResponse:
        try:
            self.observability.log_controller_in()
            member_id = request.data.get("member_id")

            if member_id is None:
                raise MissingParameters("member_id")

            if not isinstance(member_id, str): 
                raise WrongTypeParameter(
                    fieldName="member_id",
                    fieldTypeExpected="str",
                    fieldTypeReceived=type(member_id).__name__,
                )

            member = self.GetMemberUsecase(member_id=member_id)
            viewmodel = GetMemberViewmodel(member)

            response = OK(viewmodel.to_dict())
            self.observability.log_controller_out(input=member.member_id)
            return response

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

        except Exception as err:
            self.observability.log_exception(message=err.args[0])
            return InternalServerError(body=err.args[0])
