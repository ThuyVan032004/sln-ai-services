from cqrs import RequestMediator
from dependency_injector.containers import DynamicContainer
from dependency_injector import providers

from data.db_session import ObjectRecognitionDbSession
from data.unit_of_work import ObjectRecognitionUnitOfWork
from data.repository import ObjectRecognitionRepository
from shared.src.host.service_provider import add_application_services, add_domain_services

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
        
        self.mediator = providers.Factory(RequestMediator)
        
        add_application_services(self)
        add_domain_services(self)
    
container = Container()
    
    
    

    