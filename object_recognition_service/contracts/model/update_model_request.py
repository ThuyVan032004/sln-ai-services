from typing import Optional

from data.enums.model_enum import ModelStatus
from shared.contracts.requests.update_request import UpdateRequest, UpdateResponse


class UpdateModelRequest(UpdateRequest):
    id: str
    name: Optional[str]
    checkpoint_uri: Optional[str] 
    status: Optional[ModelStatus]

class UpdateModelResponse(UpdateResponse):
    id: str
    name: str
    checkpoint_uri: str
    status: ModelStatus