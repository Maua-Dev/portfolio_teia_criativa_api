from urllib.parse import urlparse

from src.modules.create_member.app.create_member_usecase import CreateMemberUsecase
from src.modules.create_member.app.create_member_viewmodel import CreateMemberViewModel
from src.shared.helpers.auth.authorizer_user import USER_FROM_AUTHORIZER_KEY
from src.shared.helpers.errors.controller_errors import InvalidImageUrl, MissingParameters, WrongTypeParameter
from src.shared.helpers.errors.domain_errors import EntityError
from src.shared.helpers.errors.usecase_errors import ForbiddenAction, NoItemsFound
from src.shared.helpers.external_interfaces.external_interface import IRequest, IResponse
from src.shared.helpers.external_interfaces.http_codes import BadRequest, Created, Forbidden, InternalServerError, NotFound


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

            if not isinstance(member_photo, str):
                raise WrongTypeParameter(
                    fieldName='member_photo',
                    fieldTypeExpected='str',
                    fieldTypeReceived=type(member_photo).__name__
                )

            parsed_url = urlparse(member_photo)
            if (
                parsed_url.scheme not in ("http", "https")
                or not parsed_url.netloc
                or not parsed_url.path.lower().endswith((".jpg", ".jpeg"))
            ):
                raise InvalidImageUrl(
                    "member_photo must be a valid URL pointing to a JPG or JPEG image"
                )

            if member_name is None:
                raise MissingParameters('member_name')
            if not isinstance(member_name, str):
                raise WrongTypeParameter(
                    fieldName='member_name',
                    fieldTypeExpected='str',
                    fieldTypeReceived=type(member_name).__name__
                )

            if member_intro is None:
                raise MissingParameters('member_intro')

            if not isinstance(member_intro, str):
                raise WrongTypeParameter(
                    fieldName='member_intro',
                    fieldTypeExpected='str',
                    fieldTypeReceived=type(member_intro).__name__
                )

            member = self.CreateMemberUsecase(
                member_photo=member_photo,
                member_name=member_name,
                member_intro=member_intro,
                requester_id=self._get_requester_id(request)
            )

            viewmodel = CreateMemberViewModel(member)
            return Created(viewmodel.to_dict())

        except NoItemsFound as err:
            return NotFound(body=err.message)

        except ForbiddenAction as err:
            return Forbidden(body=err.message)

        except MissingParameters as err:
            return BadRequest(body=err.message)

        except WrongTypeParameter as err:
            return BadRequest(body=err.message)

        except InvalidImageUrl as err:
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

        sub = authorizer_user.get("sub", None)
        return sub if isinstance(sub, str) else None