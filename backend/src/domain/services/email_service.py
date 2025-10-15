import asyncio
from datetime import datetime

from src.domain.aggregates.imap.entities import IMAP
from src.domain.aggregates.imap.exceptions import IMAPNotFoundForEmailDomain
from src.domain.aggregates.imap.repository import IMAPRepository
from src.domain.shared.interfaces.email_client.exceptions import (
    AuthPlatformChallengeCodeNotFound,
    PasswordChangeMessageNotFound,
)
from src.domain.shared.interfaces.logger import Logger
from src.infrastructure.email_client.client import DefaultEmailClient
from src.infrastructure.email_client.utils import parse_email_domain


class EmailServiceFactory:

    def __init__(self, imap_repository: IMAPRepository):
        self._imap_repository = imap_repository

    def create(self, logger) -> "EmailService":
        return EmailService(
            logger=logger,
            imap_repository=self._imap_repository,
        )


class EmailService:
    def __init__(
        self,
        logger: Logger,
        imap_repository: IMAPRepository,
    ):
        self.logger = logger
        self.client = DefaultEmailClient()
        self._imap_repository = imap_repository

    async def wait_for_reset_link(
        self,
        username: str,
        password: str,
        from_datetime: datetime,
        delay: int = 10,
        retries: int = 3,
        from_email: str = "security@mail.instagram.com",
    ) -> str:
        imap = await self._get_imap_for_domain(parse_email_domain(username))
        for i in range(retries):
            await self.logger.info("Ожидание письма со ссылкой сброса...")
            await asyncio.sleep(5 if i == 0 else delay)
            link = await self.client.get_reset_password_link(
                username=username,
                password=password,
                from_email=from_email,
                imap=imap,
                cutoff=from_datetime,
            )
            if link:
                return link

        raise PasswordChangeMessageNotFound()

    async def wait_for_auth_challenge_code(
        self,
        username: str,
        password: str,
        from_datetime: datetime,
        delay: int = 10,
        retries: int = 20,
        from_email: str = "security@mail.instagram.com",
    ) -> str:
        imap = await self._get_imap_for_domain(parse_email_domain(username))
        for i in range(retries):
            await self.logger.info("Ожидание письма с кодом подтверждения...")
            await asyncio.sleep(5 if i == 0 else delay)
            try:
                code = await self.client.get_auth_platform_code(
                    username=username,
                    password=password,
                    from_email=from_email,
                    imap=imap,
                    cutoff=from_datetime,
                )
                if code:
                    return code
            except Exception as e:
                await self.logger.warning(f"Ошибка при получении кода: {e}")

        raise AuthPlatformChallengeCodeNotFound()

    async def _get_imap_for_domain(self, domain: str) -> IMAP:
        imap = await self._imap_repository.get_by_domain(domain)
        if not imap:
            raise IMAPNotFoundForEmailDomain(domain=domain)
        return imap
