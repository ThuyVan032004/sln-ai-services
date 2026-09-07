from typing import List

from pydantic import BaseModel, ConfigDict
from fastapi import File, UploadFile


from shared.contracts.requests import CreateRequest, CreateResponse

class CreatePredictionDto(BaseModel):
    prediction: str
    confidence: float
    bbox_x: float
    bbox_y: float
    bbox_width: float
    bbox_height: float
    
class CreatePredictionRequest(CreateRequest):
    file: UploadFile = File(..., description="The image file to be uploaded.")

class CreatePredictionResponse(CreateResponse):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    predictions: List[CreatePredictionDto]
    