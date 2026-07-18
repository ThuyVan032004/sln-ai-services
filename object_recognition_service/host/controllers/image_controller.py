from cqrs import RequestMediator
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from contracts.image.create_image_request import CreateImageRequest, CreateImageResponse
from host.container import container

router = APIRouter(prefix="/images")

class ImageController:
    @staticmethod
    @router.post("")
    @inject
    async def create(
        request: CreateImageRequest, 
        mediator: RequestMediator = Depends(Provide[container.mediator])
    ) -> CreateImageResponse:
        return await mediator.send(request)
