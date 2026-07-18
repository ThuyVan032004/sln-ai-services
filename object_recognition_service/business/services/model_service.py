from dependency_injector.wiring import inject, Provide

from business.application_service import ObjectRecognitionApplicationService
from contracts.model.create_model_request import CreateModelRequest, CreateModelResponse
from contracts.model.get_detail_model_request import GetDetailModelRequest, GetDetailModelResponse
from contracts.model.update_model_request import UpdateModelRequest, UpdateModelResponse
from contracts.model.delete_model_request import DeleteModelRequest, DeleteModelResponse
from fastapi import HTTPException, status
# from host.container import container

class ModelService(ObjectRecognitionApplicationService):
    @inject
    def __init__(self, model_manager = Provide["model_manager"]):
        super().__init__(unit_of_work=Provide["unit_of_work"])
        self.model_manager = model_manager
    
    def create(self, request: CreateModelRequest) -> CreateModelResponse:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
    
    def get_detail(self, request: GetDetailModelRequest) -> GetDetailModelResponse:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
    
    def update(self, request: UpdateModelRequest) -> UpdateModelResponse:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
    
    def delete(self, request: DeleteModelRequest) -> DeleteModelResponse:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)