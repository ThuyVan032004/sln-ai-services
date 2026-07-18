from cqrs import RequestMediator
from fastapi import APIRouter, Depends
from dependency_injector.wiring import Provide, inject
from object_recognition_service.contracts.image.create_image_request import CreateImageRequest, CreateImageResponse
# from host.container import container

router = APIRouter(prefix="/images")

class ImageController:
    @staticmethod
    @router.post("")
    @inject
    async def create(
        request: CreateImageRequest = Depends(),
        mediator: RequestMediator = Depends(Provide["mediator"])
    ) -> CreateImageResponse:
        return await mediator.send(request)
