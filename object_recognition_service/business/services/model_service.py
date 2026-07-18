from dependency_injector.wiring import inject, Provide

from business.application_service import ObjectRecognitionApplicationService
from contracts.model.create_model_request import CreateModelRequest, CreateModelResponse
from contracts.model.get_detail_model_request import GetDetailModelRequest, GetDetailModelResponse
from contracts.model.update_model_request import UpdateModelRequest, UpdateModelResponse
from contracts.model.delete_model_request import DeleteModelRequest, DeleteModelResponse
from host.container import container

class ModelService(ObjectRecognitionApplicationService):
    @inject
    def __init__(self, model_manager = Provide[container.model_manager]):
        self.model_manager = model_manager
    
    def create(self, request: CreateModelRequest) -> CreateModelResponse:
        return self.model_manager.create(request)
    
    def get_detail(self, request: GetDetailModelRequest) -> GetDetailModelResponse:
        return self.model_manager.get_detail(request)
    
    def update(self, request: UpdateModelRequest) -> UpdateModelResponse:
        return self.model_manager.update(request)
    
    def delete(self, request: DeleteModelRequest) -> DeleteModelResponse:
        return self.model_manager.delete(request)