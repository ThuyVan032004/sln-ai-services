import asyncio
import io
import logging
import time
from fastapi import HTTPException
from sqlalchemy import and_

from common.constants import YOLO_CLASS_NAMES
from data.entities.model import Model
from sqlalchemy import and_
from object_recognition_service.data.enums.model_enum import ModelStatus
from PIL import Image

from dependency_injector.wiring import inject, Provide

from object_recognition_service.business.application_service import ObjectRecognitionApplicationService
from object_recognition_service.contracts.prediction.create_prediction_request import CreatePredictionDto, CreatePredictionRequest, CreatePredictionResponse

logger = logging.getLogger(__name__)
class PredictionService(ObjectRecognitionApplicationService):
    @inject
    def __init__(
        self, 
        category_manager = Provide["category_manager"],
        model_manager = Provide["model_manager"],
        unit_of_work = Provide["unit_of_work"]
    ):
        super().__init__(unit_of_work=unit_of_work)
        self.category_manager = category_manager
        self.model_manager = model_manager

    async def create(self, request: CreatePredictionRequest) -> CreatePredictionResponse:
        start = time.time()
        file = request.file
        file_content = await file.read()
        
        image = Image.open(io.BytesIO(file_content)).convert("RGB")

        detection_image = image.resize((640, 640))  # resize cho detection
        from object_recognition_service.host.main import app  # Import app from main.py
        detections = (await asyncio.to_thread(
            app.detection_model.predict,
            [detection_image],
        ))[0]  # first (only) image's result

        boxes = detections["boxes_xyxy"]
        confidences = detections["confidences"]
        class_ids = detections["class_ids"]

        prediction_dtos = [None] * len(boxes)
        recognition_batches = {}
        for detection_index, (box, det_confidence, class_id) in enumerate(zip(boxes, confidences, class_ids)):
            x1, y1, x2, y2 = box
            bbox_x = int(x1)
            bbox_y = int(y1)
            bbox_width = int(x2 - x1)
            bbox_height = int(y2 - y1)

            class_id = int(class_id)  # 15.0 -> 15
            class_name = YOLO_CLASS_NAMES.get(class_id, "unknown")

            recognition_model = await self.model_manager.find_by(
                and_(
                    Model.object_class == class_name,
                    Model.model_type == "recognition",
                    Model.status == ModelStatus.READY,
                )
            )
            
            if recognition_model is None:
                prediction_dto = CreatePredictionDto(
                    prediction="unknown",
                    confidence=det_confidence,
                    bbox_x=bbox_x,
                    bbox_y=bbox_y,
                    bbox_width=bbox_width,
                    bbox_height=bbox_height,
                )
                prediction_dtos[detection_index] = prediction_dto
                continue  # Skip this detection if no recognition model is found
            
            model_name = recognition_model.model_name
            cached_model = app.recognition_model_cache.get(model_name)

            if cached_model is None:
                return HTTPException(status_code=500, detail=f"Recognition model not found.")

            loaded_recognition_model = cached_model

            batch = recognition_batches.setdefault(model_name, {
                "model": loaded_recognition_model,
                "images": [],
                "detections": [],
            })
            batch["images"].append(
                image.crop((bbox_x, bbox_y, bbox_x + bbox_width, bbox_y + bbox_height))
            )
            batch["detections"].append(
                (detection_index, bbox_x, bbox_y, bbox_width, bbox_height)
            )

        async def predict_batch(batch):
            def predict_one_at_a_time():
                results = []
                for image in batch["images"]:
                    results.extend(batch["model"].predict([image]))
                return results

            return await asyncio.to_thread(predict_one_at_a_time)

        recognition_results_by_batch = await asyncio.gather(*(
            predict_batch(batch)
            for batch in recognition_batches.values()
        ))

        for batch, recognition_results in zip(
            recognition_batches.values(),
            recognition_results_by_batch,
        ):
            for result, detection in zip(
                recognition_results,
                batch["detections"],
            ):
                detection_index, bbox_x, bbox_y, bbox_width, bbox_height = detection
                prediction_dtos[detection_index] = CreatePredictionDto(
                    prediction=result.get("pred", "unknown"),
                    confidence=result.get("conf", 0.0),
                    bbox_x=bbox_x,
                    bbox_y=bbox_y,
                    bbox_width=bbox_width,
                    bbox_height=bbox_height,
                )

        end = time.time()
        logger.info(f"Prediction took {end - start:.2f} seconds.")
            
        return CreatePredictionResponse(
            predictions=[dto for dto in prediction_dtos if dto is not None]
        )
    
    