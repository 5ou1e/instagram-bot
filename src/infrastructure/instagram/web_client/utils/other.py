from src.domain.shared.interfaces.email_client.exceptions import (
    IncorrectEmailStringError,
)


def match_masked_email(masked: str, real: str) -> bool:
    try:
        masked_local, masked_domain = masked.split("@")
        real_local, real_domain = real.split("@")
    except Exception as e:
        raise IncorrectEmailStringError(email=real)

    # Проверка локальной части (до @)
    if masked_local[0] != real_local[0] or masked_local[-1] != real_local[-1]:
        return False
    if len(masked_local) != len(real_local):
        return False

    # Проверка доменной части (после @)
    real_domain_parts = real_domain.split(".")
    masked_domain_parts = masked_domain.split(".")
    # Первая часть домена должна совпадать по началу и длине
    if masked_domain_parts[0][0] != real_domain_parts[0][0]:
        return False

    # Расширение домена (.com и т.д.) должно совпадать
    if masked_domain_parts[-1] != real_domain_parts[-1]:
        return False

    return True
