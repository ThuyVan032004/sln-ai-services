from typing import List
from uuid import UUID

from data.entities.prediction import Prediction
from pydantic import BaseModel, ConfigDict
from fastapi import File, UploadFile


from shared.contracts.requests.create_request import CreateRequest, CreateResponse

class CreatePredictionDto(BaseModel):
    prediction: str
    confidence: float
    bbox_x: float
    bbox_y: float
    bbox_width: float
    bbox_height: float
    
class CreatePredictionRequest(CreateRequest):
    # image_id: str
    file: UploadFile = File(..., description="The image file to be uploaded.")

class CreatePredictionResponse(CreateResponse):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    predictions: List[CreatePredictionDto]
    