import random
import string


def generate_login() -> str:
    """Генерирует случайный логин"""
    words = [
        "cool", "super", "mega", "pro", "best", "top", "real", "new", "old", "big",
        "small", "fast", "slow", "hot", "cold", "dark", "light", "red", "blue", "green",
        "black", "white", "young", "gold", "silver", "star", "moon", "sun", "fire", "ice",
        "wild", "free", "true", "magic", "power", "strong", "smart", "brave", "lucky", "happy"
    ]

    patterns = [
        lambda: random.choice(words) + str(random.randint(100, 9999)),
        lambda: random.choice(words) + "_" + random.choice(words),
        lambda: random.choice(words) + random.choice(["123", "777", "999", "2024", "2025"]),
        lambda: ''.join(random.choices(string.ascii_lowercase, k=random.randint(6, 10))) + str(
            random.randint(10, 99))
    ]

    return random.choice(patterns)()


def generate_password() -> str:
    """Генерирует случайный пароль"""
    length = random.randint(8, 12)
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


def generate_accounts(count: int) -> None:
    """Генерирует и выводит N аккаунтов в формате login:password"""
    for _ in range(count):
        login = generate_login()
        password = generate_password()
        print(f"{login}:{password}")


if __name__ == "__main__":
    # Генерируем 10 аккаунтов
    generate_accounts(10_000)
    