from typing import Type, TypeVar

from business.mlflow_service import MlflowService
from object_recognition_service.data.entities.category import Category
from object_recognition_service.data.entities.model import Model

from object_recognition_service.contracts.prediction.create_prediction_request import CreatePredictionRequest
from cqrs import RequestMap, RequestMediator
from dependency_injector.containers import DynamicContainer
from dependency_injector import providers

from object_recognition_service.data.db_session import ObjectRecognitionDbSession
from object_recognition_service.data.unit_of_work import ObjectRecognitionUnitOfWork
from object_recognition_service.data.repository import ObjectRecognitionRepository
from object_recognition_service.host.request_handlers.create_prediction_request_handler import CreatePredictionRequestHandler
from shared.host.service_provider import add_application_services, add_domain_services, add_mlflow_service, add_request_handlers

T = TypeVar("T")

class Container(DynamicContainer):
    def __init__(self):
        super().__init__()
        
        self.db_session = providers.Factory(ObjectRecognitionDbSession) 
        self.unit_of_work = providers.Factory(
            ObjectRecognitionUnitOfWork,
            self.db_session
        )
        self.model_repository = providers.Factory(
            ObjectRecognitionRepository,
            db_session=self.db_session,
            entity_type=Model
        )
        self.category_repository = providers.Factory(
            ObjectRecognitionRepository,
            db_session=self.db_session,
            entity_type=Category
        )
        
        request_map = RequestMap()
        request_map.bind(CreatePredictionRequest, CreatePredictionRequestHandler)

        self.mediator = providers.Factory(
            RequestMediator,
            request_map,
            self
        )
        
        self.mlflow_service = providers.Singleton(
            MlflowService
        )
    
    @staticmethod
    def create_repository(db_session_provider, entity_type):
        repo = ObjectRecognitionRepository(db_session_provider)
        repo._entity_type = entity_type
        return repo
        
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
# add_mlflow_service(container)

container.wire(modules=[
    "object_recognition_service.host.controllers.prediction_controller",
    
    "object_recognition_service.host.request_handlers.create_prediction_request_handler",
    
    "object_recognition_service.business.services.prediction_service",
    
    "object_recognition_service.business.managers.model_manager",
    "object_recognition_service.business.managers.category_manager",
])


    


    