import io
import os
from typing import List
from sqlalchemy import and_

from business.mlflow_service import MlflowService
from common.constants import YOLO_CLASS_NAMES
from data.entities.category import Category
from data.entities.model import Model
from sqlalchemy import and_
from object_recognition_service.data.enums.model_enum import ModelStatus
import mlflow
from PIL import Image
from uuid import uuid4

from object_recognition_service.business.services.helpers.s3_helper import download_image_from_s3
from shared.common.constants.env_constants import EnvConstants
from object_recognition_service.data.entities.prediction import Prediction
from dependency_injector.wiring import inject, Provide

from object_recognition_service.business.application_service import ObjectRecognitionApplicationService
from object_recognition_service.data.entities.image import Image as ImageEntity
from object_recognition_service.contracts.prediction.create_prediction_request import CreatePredictionDto, CreatePredictionRequest, CreatePredictionResponse
from object_recognition_service.contracts.prediction.update_prediction_request import UpdatePredictionRequest, UpdatePredictionResponse
from fastapi import HTTPException, status
# from host.container import container

class PredictionService(ObjectRecognitionApplicationService):
    @inject
    def __init__(
        self, 
        prediction_manager = Provide["prediction_manager"],
        image_manager = Provide["image_manager"], 
        category_manager = Provide["category_manager"],
        model_manager = Provide["model_manager"],
        mlflow_service: MlflowService = Provide["mlflow_service"],
        unit_of_work = Provide["unit_of_work"]
    ):
        super().__init__(unit_of_work=unit_of_work)
        self.prediction_manager = prediction_manager
        self.image_manager = image_manager
        self.mlflow_service = mlflow_service
        self.category_manager = category_manager
        self.model_manager = model_manager

    # async def create(self, request: CreatePredictionRequest) -> CreatePredictionResponse:
    #     object_detection_model_name = os.getenv(EnvConstants.OBJECT_DETECTION_MODEL_NAME)
    #     recognition_model_stage = os.getenv(EnvConstants.OBJECT_RECOGNITION_MODEL_STAGE)
    #     model_stage = os.getenv(EnvConstants.OBJECT_DETECTION_MODEL_STAGE)
    #     bucket_name = os.getenv(EnvConstants.AWS_S3_BUCKET)
    #     region_name = os.getenv(EnvConstants.AWS_REGION)
        
    #     request_image = await self.image_manager.find_by(ImageEntity.id==request.image_id)
        
    #     if request_image is None:
    #         raise ValueError(f"Image not found: {request.image_id}")

    #     # 1. Load the raw image bytes from S3
    #     image_bytes = await download_image_from_s3(
    #         object_key=request_image.file_path,
    #         bucket_name=bucket_name,
    #         region_name=region_name,
    #     )
    #     image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    #     detection_model = self.mlflow_service.load_model(object_detection_model_name, "production")
        
    #     detections = detection_model.predict([image])[0]  # first (only) image's result

    #     boxes = detections["boxes_xyxy"]
    #     confidences = detections["confidences"]
    #     class_ids = detections["class_ids"]

    #     predictions: List[Prediction] = []
    #     prediction_dtos = []
    #     for box, det_confidence, class_id in zip(boxes, confidences, class_ids):
    #         x1, y1, x2, y2 = box
    #         bbox_x = int(x1)
    #         bbox_y = int(y1)
    #         bbox_width = int(x2 - x1)
    #         bbox_height = int(y2 - y1)

    #         class_id = int(class_id)  # 15.0 -> 15
    #         class_name = YOLO_CLASS_NAMES.get(class_id, "unknown")

    #         recognition_model = await self.model_manager.find_by(
    #             and_(
    #                 Model.object_class == class_name,
    #                 Model.model_type == "recognition",
    #                 Model.status == ModelStatus.READY,
    #             )
    #         )
            
    #         if recognition_model is None:
    #             prediction_dto = CreatePredictionDto(
    #                 image_id=request.image_id,
    #                 prediction="unknown",
    #                 confidence=det_confidence,
    #                 bbox_x=bbox_x,
    #                 bbox_y=bbox_y,
    #                 bbox_width=bbox_width,
    #                 bbox_height=bbox_height,
    #             )
    #             prediction_dtos.append(prediction_dto)
    #             continue  # Skip this detection if no recognition model is found

    #         print(f"Using recognition model '{recognition_model.model_name}' for object class '{class_name}'")
    #         loaded_recognition_model = self.mlflow_service.load_model(
    #             recognition_model.model_name, "production"
    #         )

    #         cropped_image = image.crop((bbox_x, bbox_y, bbox_x + bbox_width, bbox_y + bbox_height))

    #         recognition_result = loaded_recognition_model.predict([cropped_image])
    #         print(f"Recognition result for object class '{class_name}': {recognition_result}")
    #         label = recognition_result[0]["pred"] if recognition_result else "unknown"

    #         detection_model_entity = await self.model_manager.find_by(
    #             and_(
    #                 Model.model_name == object_detection_model_name,
    #                 Model.model_type == "detection",
    #                 Model.status == ModelStatus.READY,
    #             )
    #         )
            
    #         category_entity = await self.category_manager.find_by(Category.member == label)

            
    #         prediction = Prediction(
    #             id=uuid4(),
    #             detection_model_id=detection_model_entity.id,      # see note below
    #             recognition_model_id=recognition_model.id,        # DB entity, not loaded model
    #             image_id=request.image_id,
    #             category_id=category_entity.id if category_entity else None,
    #             confidence=recognition_result[0]["conf"] if recognition_result else 0.0,
    #             bbox_x=bbox_x,
    #             bbox_y=bbox_y,
    #             bbox_width=bbox_width,
    #             bbox_height=bbox_height,
    #         )
            
    #         prediction_dto = CreatePredictionDto(
    #             image_id=request.image_id,
    #             prediction=label,
    #             confidence=recognition_result[0]["conf"] if recognition_result else 0.0,
    #             bbox_x=bbox_x,
    #             bbox_y=bbox_y,
    #             bbox_width=bbox_width,
    #             bbox_height=bbox_height,
    #         )
            
    #         predictions.append(prediction)
    #         prediction_dtos.append(prediction_dto)
            
    #     await self.prediction_manager.add_range(predictions)
    #     await self.unit_of_work.commit()
            
    #     return CreatePredictionResponse(predictions=prediction_dtos)
    
    async def create(self, request: CreatePredictionRequest) -> CreatePredictionResponse:
        object_detection_model_name = os.getenv(EnvConstants.OBJECT_DETECTION_MODEL_NAME)
        
        file = request.file
        file_content = await file.read()
        
        image = Image.open(io.BytesIO(file_content)).convert("RGB")

        detection_model = self.mlflow_service.load_model(object_detection_model_name, "production")
        
        detections = detection_model.predict([image])[0]  # first (only) image's result

        boxes = detections["boxes_xyxy"]
        confidences = detections["confidences"]
        class_ids = detections["class_ids"]

        prediction_dtos = []
        for box, det_confidence, class_id in zip(boxes, confidences, class_ids):
            x1, y1, x2, y2 = box
            bbox_x = int(x1)
            bbox_y = int(y1)
            bbox_width = int(x2 - x1)
            bbox_height = int(y2 - y1)

            class_id = int(class_id)  # 15.0 -> 15
            class_name = YOLO_CLASS_NAMES.get(class_id, "unknown")
            
            print(f"Detected object class '{class_name}' with confidence {det_confidence}")

            recognition_model = await self.model_manager.find_by(
                and_(
                    Model.object_class == class_name,
                    Model.model_type == "recognition",
                    Model.status == ModelStatus.READY,
                )
            )
            
            if recognition_model is None:
                print("Code is in this block")
                prediction_dto = CreatePredictionDto(
                    prediction="unknown",
                    confidence=det_confidence,
                    bbox_x=bbox_x,
                    bbox_y=bbox_y,
                    bbox_width=bbox_width,
                    bbox_height=bbox_height,
                )
                prediction_dtos.append(prediction_dto)
                continue  # Skip this detection if no recognition model is found

            print(f"Using recognition model '{recognition_model.model_name}' for object class '{class_name}'")
            loaded_recognition_model = self.mlflow_service.load_model(
                recognition_model.model_name, "production"
            )

            cropped_image = image.crop((bbox_x, bbox_y, bbox_x + bbox_width, bbox_y + bbox_height))

            recognition_result = loaded_recognition_model.predict([cropped_image])
            print(f"Recognition result for object class '{class_name}': {recognition_result}")
            label = recognition_result[0]["pred"] if recognition_result else "unknown"

            prediction_dto = CreatePredictionDto(
                prediction=label,
                confidence=recognition_result[0]["conf"] if recognition_result else 0.0,
                bbox_x=bbox_x,
                bbox_y=bbox_y,
                bbox_width=bbox_width,
                bbox_height=bbox_height,
            )
            
            prediction_dtos.append(prediction_dto)
            
        return CreatePredictionResponse(predictions=prediction_dtos)
        
    
    async def update(self, request: UpdatePredictionRequest) -> UpdatePredictionResponse:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED)
    
    