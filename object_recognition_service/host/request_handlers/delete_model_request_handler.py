from cqrs import RequestHandler
from dependency_injector.wiring import inject, Provide

from contracts.model.delete_model_request import DeleteModelRequest, DeleteModelResponse
# from host.container import container


class DeleteModelRequestHandler(RequestHandler[DeleteModelRequest, DeleteModelResponse]):
    @inject
    def __init__(self, model_service = Provide["model_service"]):
        self.model_service = model_service

    async def handle(self, request: DeleteModelRequest) -> DeleteModelResponse:
        return await self.model_service.delete(request)