from bs4 import BeautifulSoup

from src.domain.shared.interfaces.email_client.exceptions import BadEmailError


async def parse_url_from_html_message(html: str):
    soup = BeautifulSoup(html, "html.parser")
    links = soup.find_all("a", href=True)

    for link in links:
        href = link["href"]
        if "instagram.com/accounts/password/reset/confirm/" in href:
            return href
    return None


async def parse_auth_platform_code_from_message(html: str):
    soup = BeautifulSoup(html, "html.parser")
    # находим первый <font> с атрибутом size="6"
    font_tag = soup.find("font", attrs={"size": "6"})
    # возвращаем текст — сам шестизначный код
    if not font_tag:
        return None
    return font_tag.get_text(strip=True)


def parse_email_domain(email: str) -> str:
    try:
        return email.split("@")[-1]
    except Exception as e:
        raise BadEmailError(email=email)
