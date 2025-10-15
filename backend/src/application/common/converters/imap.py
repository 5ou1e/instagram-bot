import uuid

from src.application.common.exceptions import IncorrectIMAPStringFormatError
from src.domain.aggregates.imap.entities import IMAP


def convert_imap_line_to_entity(line: str) -> IMAP:
    """
    Парсит строку вида "domain:host:port" и возвращает IMAP-entity.
    Пробельные символы вокруг частей строки учитываются автоматически.
    """
    # Обрезаем пробельные символы и пропускаем пустые строки
    line = line.strip()
    if not line:
        raise IncorrectIMAPStringFormatError(
            string=line,
        )

    parts = line.split(":")
    if len(parts) != 3:
        raise IncorrectIMAPStringFormatError(
            string=line,
        )

    domain, host, port_str = (p.strip() for p in parts)
    try:
        port = int(port_str)
    except ValueError:
        raise IncorrectIMAPStringFormatError(
            string=line,
        )

    return IMAP(id=uuid.uuid4(), domain=domain, host=host, port=port)
