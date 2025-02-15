from fastapi import Depends

from src.dto.distribution_response_dto import DistributionResponseDTO
from src.service.distribution_service import DistributionService, get_distribution_service


class DistributionController:
    def __init__(self, distribution_service: DistributionService):
        self.distribution_service = distribution_service

    def distribute_orders(self):
        return DistributionResponseDTO.from_dict(
            self.distribution_service.distribute_orders()
        )


def get_distribution_controller(
    distribution_service: DistributionService = Depends(get_distribution_service),
) -> DistributionController:
    return DistributionController(distribution_service)
