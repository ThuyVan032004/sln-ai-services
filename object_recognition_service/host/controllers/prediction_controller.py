from cqrs import RequestMediator
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from object_recognition_service.contracts.prediction import CreatePredictionRequest, CreatePredictionResponse
from object_recognition_service.host import container

router = APIRouter(prefix="/predictions")

class PredictionController:
    @staticmethod
    @router.post("")
    @inject
    async def create(
        request: CreatePredictionRequest = Depends(),
        mediator: RequestMediator = Depends(Provide[container.mediator])
    ) -> CreatePredictionResponse:
        return await mediator.send(request)