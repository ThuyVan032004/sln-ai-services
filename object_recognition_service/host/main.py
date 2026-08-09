import uvicorn
from fastapi import FastAPI

from object_recognition_service.host.controllers import image_controller
from object_recognition_service.host.controllers import model_controller
from object_recognition_service.host.controllers import prediction_controller

def create_app() -> FastAPI:
    """Hàm khởi tạo ứng dụng FastAPI"""
    
    app = FastAPI(
        title="Object Recognition API",
        version="1.0.0"
    )

    app.include_router(
        image_controller.router, 
        tags=["Images"]
    )
    
    app.include_router(
        model_controller.router,  
        tags=["Models"]
    )
    
    app.include_router(
        prediction_controller.router, 
        tags=["Predictions"]
    )

    return app

# Tạo instance của ứng dụng
app = create_app()

@app.get("/", tags=["Health Check"])
def health_check():
    """Đầu mỗn kiểm tra trạng thái API"""
    return {"status": "ok", "message": "Object Recognition API is running!"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8786, reload=True)