import re

from uuid6 import uuid7

from src.application.common.exceptions import IncorrectProxyStringFormatError
from src.domain.proxy.entities import Proxy, ProxyProtocol

PROXY_PATTERN = re.compile(
    r"""
    ^\s*
    # необязательный protocol + separator (:// или :)
    (?:(?P<protocol>https?)(?:://|:))?
    # необязательные credentials user:pass@
    (?:(?P<u1>[^:@\s]+):(?P<p1>[^@:\s]+)@)?
    # хост (например pr.oxylabs.io)
    (?P<host>[\w\.-]+)
    :
    # порт
    (?P<port>\d{1,5})
    # необязательный формат :user:pass в конце
    (?::(?P<u2>[^:\s]+):(?P<p2>[^:\s]+))?
    \s*$
    """,
    re.IGNORECASE | re.VERBOSE,
)


def convert_proxy_line_to_entity(line: str) -> Proxy | None:
    """
    Поддерживаем форматы:
     - [protocol://][user:pass@]host:port[:user:pass]
    """
    line = line.strip()
    if not line:
        return None

    m = PROXY_PATTERN.match(line)
    if not m:
        raise IncorrectProxyStringFormatError(string=line)

    gd = m.groupdict()
    protocol_str = (gd["protocol"] or "http").lower()

    try:
        protocol = ProxyProtocol(protocol_str)
    except Exception:
        protocol = ProxyProtocol.HTTP

    host = gd["host"]
    port = int(gd["port"])
    if not (1 <= port <= 65535):
        raise IncorrectProxyStringFormatError(string=line)

    # user/pass могут быть либо в u1/p1 (до @), либо в u2/p2 (после)
    username = gd["u1"] or gd["u2"]
    password = gd["p1"] or gd["p2"]

    return Proxy(
        id=uuid7(),
        protocol=protocol,
        host=host,
        port=port,
        username=username,
        password=password,
    )
