from typing import Optional

from shared.src.contracts.requests.create_request import CreateRequest, CreateResponse
from data.enums.model_enum import ModelStatus


class CreateModelRequest(CreateRequest):
    name: str
    checkpoint_uri: str
    status: ModelStatus
    
class CreateModelResponse(CreateResponse):
    id: str
    name: str
    checkpoint_uri: str
    status: ModelStatus