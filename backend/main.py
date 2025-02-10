from fastapi import FastAPI
from backend.routes import router

app = FastAPI(title="LogiTech API")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
