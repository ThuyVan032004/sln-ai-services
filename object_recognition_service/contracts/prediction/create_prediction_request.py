from uuid import UUID


from shared.contracts.requests.create_request import CreateRequest, CreateResponse


class CreatePredictionRequest(CreateRequest):
    image_id: UUID

class CreatePredictionResponse(CreateResponse):
    id: str
    image_id: UUID
    model_id: UUID
    category_id: UUID
    confidence: float
    bbox_x: float
    bbox_y: float
    bbox_width: float
    bbox_height: float