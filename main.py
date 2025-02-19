from backend.config import start_app
from backend.database import init_db

if __name__ == "__main__":
    import uvicorn

    init_db()
    app = start_app()
    uvicorn.run(app, host="127.0.0.1", port=8000)
