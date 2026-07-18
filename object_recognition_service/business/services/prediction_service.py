from dependency_injector.wiring import inject, Provide

from business.application_service import ObjectRecognitionApplicationService
from contracts.prediction.create_prediction_request import CreatePredictionRequest, CreatePredictionResponse
from contracts.prediction.update_prediction_request import UpdatePredictionRequest, UpdatePredictionResponse
from host.container import container

class PredictionService(ObjectRecognitionApplicationService):
    @inject
    def __init__(self, prediction_manager = Provide[container.prediction_manager]):
        self.prediction_manager = prediction_manager

    def create(self, request: CreatePredictionRequest) -> CreatePredictionResponse:
        return self.prediction_manager.create(request)
    
    def update(self, request: UpdatePredictionRequest) -> UpdatePredictionResponse:
        return self.prediction_manager.update(request)
    
    