from cqrs import RequestHandler
from dependency_injector.wiring import inject, Provide
from host.container import container

from contracts.image.create_image_request import CreateImageRequest, CreateImageResponse
from business.services.image_service import ImageService


class CreateImageRequestHandler(RequestHandler[CreateImageRequest, CreateImageResponse]):
    @inject
    def __init__(self, image_service: ImageService = Provide[container.image_service]):
        self.image_service = image_service
        
    async def handle(self, request: CreateImageRequest) -> CreateImageResponse:
        return await self.image_service.create(request)