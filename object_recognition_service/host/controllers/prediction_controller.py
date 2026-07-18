from uuid import UUID

from cqrs import RequestMediator
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from contracts.prediction.create_prediction_request import CreatePredictionRequest, CreatePredictionResponse
from contracts.prediction.update_prediction_request import UpdatePredictionRequest, UpdatePredictionResponse
from host.container import container

router = APIRouter(prefix="/predictions")

class PredictionController:
    @staticmethod
    @router.post("")
    @inject
    async def create(
        request: CreatePredictionRequest, 
        mediator: RequestMediator = Depends(Provide[container.mediator])
    ) -> CreatePredictionResponse:
        return await mediator.send(request)
    
    @staticmethod
    @router.patch("/{id}")
    @inject
    async def update(
        id: UUID,
        request: UpdatePredictionRequest, 
        mediator: RequestMediator = Depends(Provide[container.mediator])
    ) -> UpdatePredictionResponse:
        return await mediator.send(request)
