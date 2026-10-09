from src.modules.create_member.app.create_member_usecase import CreateMemberUsecase
from src.modules.create_member.app.create_member_viewmodel import CreateMemberViewModel
from src.shared.helpers.errors.controller_errors import MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, Created, InternalServerError, NotFound


class CreateMemberController:
    def __init__(self, usecase: CreateMemberUsecase):
        self.CreateMemberUsecase = usecase

    def __call__(self, request: IRequest) -> IResponse:
        try:
            member_photo = request.data.get('member_photo', None)
            member_name = request.data.get('member_name', None)
            member_intro = request.data.get('member_intro', None)

            if member_photo is None:
                raise MissingParameters('member_photo')

            if type(member_photo) != str:
                raise WrongTypeParameter(
                    fieldName='member_photo',
                    fieldTypeExpected='str',
                    fieldTypeReceived=type(member_photo).__name__
                )

            if member_name is None:
                raise MissingParameters('member_name')

            if type(member_name) != str:
                raise WrongTypeParameter(
                    fieldName='member_name',
                    fieldTypeExpected='str',
                    fieldTypeReceived=type(member_name).__name__
                )

            if member_intro is None:
                raise MissingParameters('member_intro')

            if type(member_intro) != str:
                raise WrongTypeParameter(
                    fieldName='member_intro',
                    fieldTypeExpected='str',
                    fieldTypeReceived=type(member_intro).__name__
                )

            member = self.CreateMemberUsecase(
                member_photo=member_photo,
                member_name=member_name,
                member_intro=member_intro
            )

            viewmodel = CreateMemberViewModel(member)
            return Created(viewmodel.to_dict())

        except NoItemsFound as err:
            return NotFound(body=err.message)
        
        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except EntityError as err:
            return BadRequest(body=err.message)

        except Exception as err:
            return InternalServerError(body=err)

    

    