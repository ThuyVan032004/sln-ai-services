from typing import List
from uuid import UUID

from data.entities.prediction import Prediction
from pydantic import BaseModel, ConfigDict


from shared.contracts.requests.create_request import CreateRequest, CreateResponse

class CreatePredictionDto(BaseModel):
    image_id: UUID
    prediction: str
    confidence: float
    bbox_x: float
    bbox_y: float
    bbox_width: float
    bbox_height: float
    
class CreatePredictionRequest(CreateRequest):
    image_id: str

class CreatePredictionResponse(CreateResponse):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    predictions: List[CreatePredictionDto]
    