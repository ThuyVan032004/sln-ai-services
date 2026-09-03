import os

import logging

from object_recognition_service.data.enums.model_enum import ModelStatus
from sqlalchemy import and_, select

from object_recognition_service.data.entities.model import Model
from object_recognition_service.business.mlflow_service import MlflowService
from object_recognition_service.host.container import container

from shared.common.constants.env_constants import EnvConstants
import uvicorn
from fastapi import FastAPI

from object_recognition_service.host.controllers import prediction_controller

from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    object_detection_model_name = os.getenv(
        EnvConstants.OBJECT_DETECTION_MODEL_NAME
    )

    app.mlflow_service = container.mlflow_service()
    app.detection_model = app.mlflow_service.load_model(
        object_detection_model_name,
        "production",
    )

    app.recognition_model_cache = {}

    db_session = container.db_session()
    try:
        recognition_models = await db_session.get_session().execute(
            select(Model).where(
                and_(
                    Model.model_type == "recognition",
                    Model.status == ModelStatus.READY,
                )
            )
        )

        for model in recognition_models.scalars().all():
            loaded_model = app.mlflow_service.load_model(
                model.model_name,
                "production",
            )
            if loaded_model is not None:
                app.recognition_model_cache[model.model_name] = loaded_model

        logger.info("Done app startup")
        yield
    finally:
        await db_session.get_session().close()
        await db_session._engine.dispose()

# Tạo instance của ứng dụng
app = FastAPI(
    title="Object Recognition API",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(
    prediction_controller.router, 
    tags=["Predictions"]
)

@app.get("/", tags=["Health Check"])
def health_check():
    """Đầu mỗn kiểm tra trạng thái API"""
    return {"status": "ok", "message": "Object Recognition API is running!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8786, reload=True)