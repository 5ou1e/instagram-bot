"""
Запуск CLI приложения.

Использование:
    python manage.py run [command] [options]

Пример:
    python manage.py run markets_syncer --use-proxy
    python manage.py run orderbooks_loader --no-proxy

Для получения справки по командам и опциям используйте:
    python manage.py --help
"""

from cli.main import cli

if __name__ == "__main__":
    cli()
