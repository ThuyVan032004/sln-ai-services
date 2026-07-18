from cqrs import RequestHandler
from dependency_injector.wiring import inject, Provide

from contracts.prediction.update_prediction_request import UpdatePredictionRequest, UpdatePredictionResponse
from host.container import container


class UpdatePredictionRequestHandler(RequestHandler[UpdatePredictionRequest, UpdatePredictionResponse]):
    @inject
    def __init__(self, prediction_service = Provide[container.prediction_service]):
        self.prediction_service = prediction_service

    async def handle(self, request: UpdatePredictionRequest) -> UpdatePredictionResponse:
        return await self.prediction_service.update_prediction(request)