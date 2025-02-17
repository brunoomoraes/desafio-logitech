from fastapi import FastAPI

from src.router.order_router import order_router
from src.router.truck_router import truck_router
from src.router.distribution_router import distribution_router

app = FastAPI(title="LogiTech API")

app.include_router(order_router)
app.include_router(truck_router)
app.include_router(distribution_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
