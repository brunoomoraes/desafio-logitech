from fastapi import FastAPI

from backend.routes import add_routes


def start_app() -> FastAPI:
    app = FastAPI(title="LogiTech API")
    add_routes(app)
    return app
