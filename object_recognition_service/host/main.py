import uvicorn
from fastapi import FastAPI

# 1. Import container để đảm bảo nó được khởi tạo và wire các module
# Thay 'container_config' bằng tên file chứa class Container của bạn
from host.container import container

# 2. Import các controller (nơi chứa APIRouter của FastAPI)
from host.controllers import image_controller
from host.controllers import model_controller
from host.controllers import prediction_controller

    
container.wire(modules=[
    "host.controllers.image_controller",
    "host.controllers.model_controller",
    "host.controllers.prediction_controller",
    
    "host.request_handlers.create_image_request_handler",
    "host.request_handlers.create_model_request_handler",
    "host.request_handlers.get_detail_model_request_handler",
    "host.request_handlers.delete_model_request_handler",
    "host.request_handlers.update_model_request_handler",
    "host.request_handlers.update_prediction_request_handler",
    "host.request_handlers.create_prediction_request_handler",
    
    "business.services.image_service",
    "business.services.model_service",
    "business.services.prediction_service",
    
    "business.managers.image_manager",
    "business.managers.model_manager",
    "business.managers.prediction_manager"
])

def create_app() -> FastAPI:
    """Hàm khởi tạo ứng dụng FastAPI"""
    
    app = FastAPI(
        title="Object Recognition API",
        version="1.0.0"
    )

    # 3. Đăng ký các router vào ứng dụng
    # Giả định bên trong mỗi controller có một đối tượng router = APIRouter()
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
        # tags=["Predictions"]
    )

    return app

# Tạo instance của ứng dụng
app = create_app()

@app.get("/", tags=["Health Check"])
def health_check():
    """Đầu mỗn kiểm tra trạng thái API"""
    return {"status": "ok", "message": "Object Recognition API is running!"}

if __name__ == "__main__":
    # Chạy server bằng uvicorn khi chạy trực tiếp file này
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)