from uuid import uuid4

from data.entities.prediction import Prediction
from dependency_injector.wiring import inject, Provide

from business.application_service import ObjectRecognitionApplicationService
from contracts.prediction.create_prediction_request import CreatePredictionRequest, CreatePredictionResponse
from contracts.prediction.update_prediction_request import UpdatePredictionRequest, UpdatePredictionResponse
from fastapi import HTTPException, status
# from host.container import container

class PredictionService(ObjectRecognitionApplicationService):
    @inject
    def __init__(self, prediction_manager = Provide["prediction_manager"]):
        super().__init__(unit_of_work=Provide["unit_of_work"])
        self.prediction_manager = prediction_manager

    async def create(self, request: CreatePredictionRequest) -> CreatePredictionResponse:
        prediction = Prediction(
            id=uuid4(),
            model_id="",
            image_id=request.image_id,
            category_id="",
            confidence=0.0,
            bbox_x=0.0,
            bbox_y=0.0,
            bbox_width=0.0,
            bbox_height=0.0,
        )
            
        await self.prediction_manager.create(prediction)
        await self.unit_of_work.commit()
        
        return CreatePredictionResponse(
            id=prediction.id,
            model_id=prediction.model_id,
            image_id=prediction.image_id,
            category_id=prediction.category_id,
            confidence=prediction.confidence,
            bbox_x=prediction.bbox_x,
            bbox_y=prediction.bbox_y,
            bbox_width=prediction.bbox_width,
            bbox_height=prediction.bbox_height
        )
    
    async def update(self, request: UpdatePredictionRequest) -> UpdatePredictionResponse:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
    
    