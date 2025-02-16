from backend.routes import item, service, truck


def add_routes(app):
    app.include_router(item.router, prefix="/item", tags=["Item"])
    app.include_router(truck.router, prefix="/truck", tags=["Truck"])
    app.include_router(service.router, prefix="/distribuir", tags=["Distribuir"])
