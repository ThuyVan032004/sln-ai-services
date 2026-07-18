from typing import Type, TypeVar

from object_recognition_service.contracts.image.create_image_request import CreateImageRequest
from object_recognition_service.contracts.model.create_model_request import CreateModelRequest
from object_recognition_service.contracts.model.delete_model_request import DeleteModelRequest
from object_recognition_service.contracts.model.get_detail_model_request import GetDetailModelRequest
from object_recognition_service.contracts.model.get_detail_model_request import GetDetailModelRequest
from object_recognition_service.contracts.model.update_model_request import UpdateModelRequest
from object_recognition_service.contracts.prediction.create_prediction_request import CreatePredictionRequest
from object_recognition_service.contracts.prediction.update_prediction_request import UpdatePredictionRequest
from cqrs import RequestMap, RequestMediator
from dependency_injector.containers import DynamicContainer
from dependency_injector import providers

from object_recognition_service.data.db_session import ObjectRecognitionDbSession
from object_recognition_service.data.unit_of_work import ObjectRecognitionUnitOfWork
from object_recognition_service.data.repository import ObjectRecognitionRepository
from object_recognition_service.host.request_handlers.create_image_request_handler import CreateImageRequestHandler
from object_recognition_service.host.request_handlers.create_model_request_handler import CreateModelRequestHandler
from object_recognition_service.host.request_handlers.create_prediction_request_handler import CreatePredictionRequestHandler
from object_recognition_service.host.request_handlers.delete_model_request_handler import DeleteModelRequestHandler
from object_recognition_service.host.request_handlers.get_detail_model_request_handler import GetDetailModelRequestHandler
from object_recognition_service.host.request_handlers.update_model_request_handler import UpdateModelRequestHandler
from object_recognition_service.host.request_handlers.update_prediction_request_handler import UpdatePredictionRequestHandler
from shared.src.host.service_provider import add_application_services, add_domain_services, add_request_handlers

T = TypeVar("T")

class Container(DynamicContainer):
    def __init__(self):
        super().__init__()
        
        self.db_session = providers.Singleton(ObjectRecognitionDbSession) 
        self.unit_of_work = providers.Factory(
            ObjectRecognitionUnitOfWork,
            self.db_session
        )
        self.repository = providers.Factory(
            ObjectRecognitionRepository,
            self.db_session,
        )
        
        request_map = RequestMap()
        request_map.bind(CreateImageRequest, CreateImageRequestHandler)
        request_map.bind(CreatePredictionRequest, CreatePredictionRequestHandler)
        request_map.bind(UpdatePredictionRequest, UpdatePredictionRequestHandler)
        request_map.bind(CreateModelRequest, CreateModelRequestHandler)
        request_map.bind(GetDetailModelRequest, GetDetailModelRequestHandler)
        request_map.bind(UpdateModelRequest, UpdateModelRequestHandler)
        request_map.bind(DeleteModelRequest, DeleteModelRequestHandler)
        

        self.mediator = providers.Factory(
            RequestMediator,
            request_map,
            self
        )
        
    async def resolve(self, handler_cls: Type[T]) -> T:
        """
        Lấy provider tương ứng với handler_cls đã được đăng ký trong Container
        (theo tên class) và trả về instance đã được resolve đầy đủ dependency.
        """
        provider = getattr(self, handler_cls.__name__, None)

        if provider is None:
            raise RuntimeError(
                f"Handler '{handler_cls.__name__}' chưa được đăng ký trong Container "
                f"(không tìm thấy attribute cùng tên trên container)."
            )

        if not isinstance(provider, providers.Provider):
            raise RuntimeError(
                f"Attribute '{handler_cls.__name__}' tồn tại trên Container nhưng "
                f"không phải là providers.Provider (đang là {type(provider)})."
            )

        try:
            instance = provider()
        except Exception as ex:
            raise RuntimeError(
                f"Không thể khởi tạo handler '{handler_cls.__name__}' từ provider. "
                f"Kiểm tra lại các dependency (Provide[...]) mà provider này cần — "
                f"rất có thể một sub-dependency (vd: manager/service) chưa được inject "
                f"đúng do container.wire() chưa bao phủ đúng module, hoặc provider "
                f"của dependency đó chưa được set trên Container trước khi wire()."
            ) from ex

        return instance
    
container = Container()

add_application_services(container)
add_domain_services(container)
add_request_handlers(container)

# container.wire(
#     packages=[
#         "object_recognition_service.host",      
#         "object_recognition_service.business"   
#     ]
# )

container.wire(modules=[
    "object_recognition_service.host.controllers.image_controller",
    "object_recognition_service.host.controllers.model_controller",
    "object_recognition_service.host.controllers.prediction_controller",
    
    "object_recognition_service.host.request_handlers.create_image_request_handler",
    "object_recognition_service.host.request_handlers.create_model_request_handler",
    "object_recognition_service.host.request_handlers.get_detail_model_request_handler",
    "object_recognition_service.host.request_handlers.delete_model_request_handler",
    "object_recognition_service.host.request_handlers.update_model_request_handler",
    "object_recognition_service.host.request_handlers.update_prediction_request_handler",
    "object_recognition_service.host.request_handlers.create_prediction_request_handler",
    
    "object_recognition_service.business.services.image_service",
    "object_recognition_service.business.services.model_service",
    "object_recognition_service.business.services.prediction_service",
    
    "object_recognition_service.business.managers.image_manager",
    "object_recognition_service.business.managers.model_manager",
    "object_recognition_service.business.managers.prediction_manager"
])


    


    