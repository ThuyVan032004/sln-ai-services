from uuid import UUID

from cqrs import RequestMediator
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from contracts.model.get_detail_model_request import GetDetailModelRequest, GetDetailModelResponse
from contracts.model.create_model_request import CreateModelRequest, CreateModelResponse
from contracts.model.update_model_request import UpdateModelRequest, UpdateModelResponse
from contracts.model.delete_model_request import DeleteModelRequest, DeleteModelResponse
from host.container import container


router = APIRouter(prefix="/models")

class ModelController:
    @staticmethod
    @router.get("/{id}")
    @inject
    async def get_detail(
        id: UUID,
        request: GetDetailModelRequest, 
        mediator: RequestMediator = Depends(Provide[container.mediator])
    ) -> GetDetailModelResponse:
        return await mediator.send(request)
    
    @staticmethod
    @router.post("")
    @inject
    async def create(
        request: CreateModelRequest, 
        mediator: RequestMediator = Depends(Provide[container.mediator])
    ) -> CreateModelResponse:
        return await mediator.send(request)
    
    @staticmethod
    @router.patch("/{id}")
    @inject
    async def update(
        id: UUID,
        request: UpdateModelRequest, 
        mediator: RequestMediator = Depends(Provide[container.mediator])
    ) -> UpdateModelResponse:
        return await mediator.send(request)
    
    @staticmethod
    @router.delete("/{id}")
    @inject
    async def delete(
        id: UUID,
        request: DeleteModelRequest, 
        mediator: RequestMediator = Depends(Provide[container.mediator])
    ) -> DeleteModelResponse:
        return await mediator.send(request)
