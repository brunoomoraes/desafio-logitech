from fastapi import FastAPI
from backend.routes import add_routes
from backend.database import init_db

app = FastAPI(title="LogiTech API")


if __name__ == "__main__":
    import uvicorn

    init_db()
    add_routes(app)
    uvicorn.run(app, host="127.0.0.1", port=8000)
