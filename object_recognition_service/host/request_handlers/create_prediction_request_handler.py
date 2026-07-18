from cqrs import RequestHandler
from dependency_injector.wiring import inject, Provide

from contracts.prediction.create_prediction_request import CreatePredictionRequest, CreatePredictionResponse
# from host.container import container


class CreatePredictionRequestHandler(RequestHandler[CreatePredictionRequest, CreatePredictionResponse]):
    @inject
    def __init__(self, prediction_service = Provide["prediction_service"]):
        self.prediction_service = prediction_service

    async def handle(self, request: CreatePredictionRequest) -> CreatePredictionResponse:
        return await self.prediction_service.create(request)