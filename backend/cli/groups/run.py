
import click
import uvicorn

from src.api.settings.logging import setup_logging


@click.group(help="Запустить задачу/процесс")
def run():
    pass


@run.command(name="execution")
@click.option("--host", default="127.0.0.1", help="Host address")
@click.option("--port", default=8001, help="Port number")
@click.option("--reload", is_flag=True, default=False, help="Enable auto-reload")
def run_execution_service(host, port, reload):
    setup_logging()
    uvicorn.run("src.execution_service.api.main:app", host=host, port=port, reload=reload)


@run.command(name="api")
@click.option("--host", default="127.0.0.1", help="Host address")
@click.option("--port", default=8000, help="Port number")
@click.option("--reload", is_flag=True, default=False, help="Enable auto-reload")
def run_api_server(host, port, reload):
    """Запустить FastAPI-сервер"""
    uvicorn.run("src.api.main:app", host=host, port=port, reload=reload)
