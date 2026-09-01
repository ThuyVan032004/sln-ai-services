import os
from dependency_injector.wiring import inject, Provide
from object_recognition_service.business.mlflow_service import MlflowService
from object_recognition_service.host.container import container

from shared.common.constants.env_constants import EnvConstants
import uvicorn
from fastapi import FastAPI

from object_recognition_service.host.controllers import prediction_controller

def create_app() -> FastAPI:
    """Hàm khởi tạo ứng dụng FastAPI"""
    
    app = FastAPI(
        title="Object Recognition API",
        version="1.0.0"
    )
    
    app.include_router(
        prediction_controller.router, 
        tags=["Predictions"]
    )
    
    object_detection_model_name = os.getenv(EnvConstants.OBJECT_DETECTION_MODEL_NAME)
    app.mlflow_service = container.mlflow_service()
    app.detection_model = app.mlflow_service.load_model(object_detection_model_name, "production")
    

    return app

# Tạo instance của ứng dụng
app = create_app()

@app.get("/", tags=["Health Check"])
def health_check():
    """Đầu mỗn kiểm tra trạng thái API"""
    return {"status": "ok", "message": "Object Recognition API is running!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8786, reload=True)