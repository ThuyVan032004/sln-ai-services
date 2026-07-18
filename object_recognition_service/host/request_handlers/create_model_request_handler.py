from cqrs import RequestHandler
from dependency_injector.wiring import inject, Provide

from contracts.model.create_model_request import CreateModelRequest, CreateModelResponse
# from host.container import container


class CreateModelRequestHandler(RequestHandler[CreateModelRequest, CreateModelResponse]):
    @inject
    def __init__(self, model_service = Provide["model_service"]):
        self.model_service = model_service

    async def handle(self, request: CreateModelRequest) -> CreateModelResponse:
        return await self.model_service.create(request)