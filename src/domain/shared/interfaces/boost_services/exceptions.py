class BoostServiceClientError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NoTasksError(BoostServiceClientError):
    pass


class VenroClientError(BoostServiceClientError):
    pass


class VenroBadResponseError(BoostServiceClientError):
    pass


class VenroBadApiKey(VenroClientError):
    pass


class VenroNoTasks(VenroClientError):
    pass


class VenroInvalidAccess(VenroClientError):
    pass


class VenroInvalidBotId(VenroClientError):
    pass


class VenroTaskNotAccepted(VenroClientError):
    pass


class VenroTaskAlreadySent(VenroClientError):
    pass


class VenroIncorrectTaskId(VenroClientError):
    pass


class LikebizClientError(BoostServiceClientError):
    pass


class LikebizBadApiKey(LikebizClientError):
    pass


class LikebizNoTasks(BoostServiceClientError):
    pass


class LikebizServiceNotFound(LikebizClientError):
    pass


class LikebizUnauthenticated(LikebizClientError):
    pass


class LikebizOrderIdNotFound(LikebizClientError):
    pass
