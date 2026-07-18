from cqrs import RequestHandler
from dependency_injector.wiring import inject, Provide

from contracts.model.get_detail_model_request import GetDetailModelRequest, GetDetailModelResponse
from host.container import container


class GetDetailModelRequestHandler(RequestHandler[GetDetailModelRequest, GetDetailModelResponse]):
    @inject
    def __init__(self, model_service = Provide[container.model_service]):
        self.model_service = model_service

    async def handle(self, request: GetDetailModelRequest) -> GetDetailModelResponse:
        return await self.model_service.get_detail(request)