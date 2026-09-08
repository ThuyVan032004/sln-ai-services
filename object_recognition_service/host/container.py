from typing import Type, TypeVar

from cqrs import RequestMap, RequestMediator
from dependency_injector.containers import DynamicContainer
from dependency_injector import providers
from object_recognition_service.data import ObjectRecognitionDbSession, ObjectRecognitionUnitOfWork, ObjectRecognitionRepository

T = TypeVar("T")

class Container(DynamicContainer):
    def __init__(self):
        super().__init__()
    
    def configure(self):
        self.session_factory = providers.Singleton(ObjectRecognitionDbSession)
        self.session = providers.ContextLocalSingleton(
            self.session_factory.provided.get_session.call()
        )
        self.unit_of_work = providers.Factory(
            ObjectRecognitionUnitOfWork,
            self.session
        )
        self.repository = providers.Factory(
            ObjectRecognitionRepository,
            self.session
        )
        
        self.request_map = RequestMap()
        self.mediator = providers.Factory(
            RequestMediator,
            self.request_map,
            self
        )
        
    async def resolve(self, handler_cls: Type[T]) -> T:
        provider = getattr(self, handler_cls.__name__, None)

        if provider is None:
            raise RuntimeError(
                f"Handler '{handler_cls.__name__}' is not registered."
            )

        if not isinstance(provider, providers.Provider):
            raise RuntimeError(
                f"'{handler_cls.__name__}' is not a valid provider."
            )

        try:
            return provider()
        except Exception as ex:
            raise RuntimeError(
                f"Failed to create handler '{handler_cls.__name__}'."
            ) from ex
    
    
container = Container()


    


    