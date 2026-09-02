from uuid import UUID

from cqrs import RequestMediator
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from object_recognition_service.contracts.prediction.create_prediction_request import CreatePredictionRequest, CreatePredictionResponse
from object_recognition_service.host.container import container

router = APIRouter(prefix="/predictions")

def get_mediator() -> RequestMediator:
    return container.mediator()

class PredictionController:
    @staticmethod
    @router.post("")
    async def create(
        request: CreatePredictionRequest = Depends(),
        mediator: RequestMediator = Depends(get_mediator)
    ) -> CreatePredictionResponse:
        return await mediator.send(request)