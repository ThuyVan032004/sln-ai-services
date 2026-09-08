import os

import logging

from object_recognition_service.data.enums import ModelStatus
from sqlalchemy import and_, select

from object_recognition_service.data.entities import Model
from object_recognition_service.host import container

from shared.common.constants import EnvConstants
import uvicorn
from fastapi import FastAPI

from object_recognition_service.host.controllers import prediction_controller
from shared.host import add_application_services, add_domain_services, add_mlflow_service, add_request_handlers

from contextlib import asynccontextmanager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    container.configure()
    add_application_services(container)
    add_domain_services(container)
    add_request_handlers(container, container.request_map)
    add_mlflow_service(container)
    container.wire(packages=[
        "object_recognition_service"
    ])
    object_detection_model_name = os.getenv(
        EnvConstants.OBJECT_DETECTION_MODEL_NAME
    )
    mlflow_service = container.mlflow_service()
    app.detection_model = mlflow_service.load_model(
        object_detection_model_name,
        "dev",
    )
    app.recognition_model_cache = {}
    db_session = container.session()
    try:
        recognition_models = await db_session.execute(
            select(Model).where(
                and_(
                    Model.model_type == "recognition",
                    Model.status == ModelStatus.READY,
                )
            )
        )

        for model in recognition_models.scalars().all():
            loaded_model = mlflow_service.load_model(
                model.model_name,
                "dev",
            )
            if loaded_model is not None:
                app.recognition_model_cache[model.model_name] = loaded_model

        logger.info("Done app startup")
        yield
    finally:
        await db_session.close()

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