from fastapi import FastAPI

from router.order_router import order_router

app = FastAPI(title="LogiTech API")

app.include_router(order_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
