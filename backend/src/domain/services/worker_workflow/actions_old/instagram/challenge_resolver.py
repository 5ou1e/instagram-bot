from src.domain.shared.interfaces.instagram.exceptions import ChallengeRequired


class ChallengeResolver:
    async def execute(self, challenge: ChallengeRequired):
        pass
        # if challenge.type == ChallengeType.RECAPTCHA:
        #     return PassRecaptchaChallengeActionHandler().execute()
        # else:
        #     raise NotImplemented
