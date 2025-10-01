import uvicorn

from src.api.app_factory import AppFactory

app = AppFactory.create_app()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
