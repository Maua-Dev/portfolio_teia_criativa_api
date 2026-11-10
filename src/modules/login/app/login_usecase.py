import os
import secrets
import time
from uuid import UUID

from src.shared.domain.entities.user import User
from src.shared.domain.repositories.user_repository_interface import IUserRepository
from src.shared.helpers.errors.external_errors import JwtVerificationError
from src.shared.helpers.errors.usecase_errors import (
    EnvVarNotFound,
    InvalidJwtFormat,
    NoItemsFound,
)
from src.shared.infra.external.jwt.jwt_kms_signer import JwtKmsSigner
from src.shared.infra.external.microsoft.id_token_verifier import MicrosoftIdTokenVerifier
from src.shared.infra.external.observability.observability_aws import ObservabilityAWS


class LoginUsecase:
    def __init__(
        self,
        repo: IUserRepository,
        observability: ObservabilityAWS,
        jwt_signer: JwtKmsSigner | None = None,
        ms_id_token_verifier: MicrosoftIdTokenVerifier | None = None,
    ):
        self.repo = repo
        self.observability = observability
        self.jwt_signer = jwt_signer
        self.ms_id_token_verifier = ms_id_token_verifier

    def __call__(self, id_token: str) -> tuple[str, str, User]:

        try:
            verifier = self._get_ms_id_token_verifier()
            ms_payload = verifier.verify(id_token)
            user_sub = ms_payload.get("oid")
            user_mail = ms_payload.get("preferred_username")
            user_name = ms_payload.get("name")
        except (JwtVerificationError, EnvVarNotFound) as e:
            self.observability.log_error(
                f"Falha na verificação do Microsoft id_token: {e}"
            )
            raise JwtVerificationError("Token de autenticação inválido") from e

        if not all(
            isinstance(value, str) and value
            for value in (user_sub, user_mail, user_name)
        ):
            raise InvalidJwtFormat()

        try:
            user_id = UUID(user_sub)
        except ValueError as err:
            raise InvalidJwtFormat("oid") from err

        try:
            user = self.repo.get_user(user_id=user_id)
        except NoItemsFound:
            user = self.repo.create_user(
                new_user=User(
                    id=user_id,
                    email=user_mail,
                    user_name=user_name,
                )
            )

        if not user:
            raise RuntimeError("User repository returned no user")

        access_payload = {
            "user_id": str(user.id),
            "role": user.role.value,
            "exp": int(time.time()) + (30 * 60),
        }

        access_token = self._sign_access_token(access_payload)

        refresh_token = secrets.token_hex(32)

        return access_token, refresh_token, user

    def _get_ms_id_token_verifier(self) -> MicrosoftIdTokenVerifier:
        if self.ms_id_token_verifier is not None:
            return self.ms_id_token_verifier
        return MicrosoftIdTokenVerifier(
            client_id=os.environ.get("MS_CLIENT_ID", ""),
            tenant_id=os.environ.get("MS_TENANT_ID", ""),
        )

    def _sign_access_token(self, payload: dict) -> str:
        signer = self.jwt_signer
        if signer is None:
            key_arn = os.environ.get("JWT_SIGN_KEY_ARN") or os.environ.get(
                "LOGIN_KMS_SIGN_KEY_ARN"
            )
            if not key_arn:
                raise EnvVarNotFound("JWT_SIGN_KEY_ARN")
            signer = JwtKmsSigner(key_arn=key_arn)
        return signer.sign(payload)
