from fastapi import APIRouter, Depends

from controller.distribution_controller import (
    DistributionController,
    get_distribution_controller,
)

distribution_router = APIRouter(prefix="/distribution", tags=["distribution"])


@distribution_router.get("/")
def distribute_orders(
    distribution_controller: DistributionController = Depends(
        get_distribution_controller
    ),
):
    return distribution_controller.distribute_orders()
