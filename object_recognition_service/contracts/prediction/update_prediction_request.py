from uuid import UUID

from shared.src.contracts.requests.update_request import UpdateRequest, UpdateResponse


class UpdatePredictionRequest(UpdateRequest):
    id: UUID
    image_id: UUID
    model_id: UUID
    category_id: UUID
    confidence: float
    bbox_x: float
    bbox_y: float
    bbox_width: float
    bbox_height: float

class UpdatePredictionResponse(UpdateResponse):
    id: UUID
    image_id: UUID
    model_id: UUID
    category_id: UUID
    confidence: float
    bbox_x: float
    bbox_y: float
    bbox_width: float
    bbox_height: float