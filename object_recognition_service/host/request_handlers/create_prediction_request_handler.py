from object_recognition_service.business.services import PredictionService
from cqrs import RequestHandler
from dependency_injector.wiring import inject, Provide

from object_recognition_service.contracts.prediction import CreatePredictionRequest, CreatePredictionResponse

class CreatePredictionRequestHandler(RequestHandler[CreatePredictionRequest, CreatePredictionResponse]):
    @inject
    def __init__(self, prediction_service: PredictionService = Provide["prediction_service"]):
        self.prediction_service = prediction_service

    async def handle(self, request: CreatePredictionRequest) -> CreatePredictionResponse:
        return await self.prediction_service.create(request)