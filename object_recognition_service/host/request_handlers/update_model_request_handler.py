from cqrs import RequestHandler
from dependency_injector.wiring import inject, Provide

from contracts.model.update_model_request import UpdateModelRequest, UpdateModelResponse
from host.container import container


class UpdateModelRequestHandler(RequestHandler[UpdateModelRequest, UpdateModelResponse]):
    @inject
    def __init__(self, model_service = Provide[container.model_service]):
        self.model_service = model_service

    async def handle(self, request: UpdateModelRequest) -> UpdateModelResponse:
        return await self.model_service.update(request)