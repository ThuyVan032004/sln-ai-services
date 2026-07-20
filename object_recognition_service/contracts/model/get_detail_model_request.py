from data.enums.model_enum import ModelStatus
from shared.contracts.requests.get_detail_request import GetDetailRequest, GetDetailResponse


class GetDetailModelRequest(GetDetailRequest):
    id: str

class GetDetailModelResponse(GetDetailResponse):
    id: str
    name: str
    checkpoint_uri: str
    status: ModelStatus