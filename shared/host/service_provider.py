import importlib
import inspect
import os
import pkgutil
from typing import Type
from cqrs import RequestHandler
from dependency_injector.containers import DynamicContainer
from dependency_injector.providers import Factory
from pydantic.alias_generators import to_snake

from shared.business.interfaces.application_service import IApplicationService
from shared.business.interfaces.domain_service import IDomainService
from shared.common.constants.env_constants import EnvConstants


def add_services_with_assigned_interface[T](container: DynamicContainer, interface: Type[T]):
    application_name = os.getenv(EnvConstants.APPLICATION_NAME)
    
    if application_name is None:
        raise ValueError(f"Environment variable '{EnvConstants.APPLICATION_NAME}' is not set.")
    
    application = importlib.import_module(application_name)
    
    modules = []
    for _, module_name, _ in pkgutil.walk_packages(application.__path__, prefix=f"{application_name}."):
        parts = module_name.split(".")
        
        if "entities" in parts:
            continue
            
        try:
            modules.append(importlib.import_module(module_name))
        except Exception as e:
            print(f"Cannot import module {module_name}: {e}")
    
    classes = {
        (obj.__name__ if issubclass(obj, RequestHandler) else to_snake(obj.__name__)): obj
        for module in modules
        for _, obj in inspect.getmembers(module, inspect.isclass)
        if issubclass(obj, interface) and obj is not interface and not inspect.isabstract(obj)
    }
    
    for class_name, cls in classes.items():
        print(f"Registering {cls.__name__} as {class_name} in the container.")
        setattr(container, class_name, Factory(cls))
        

def add_application_services(container: DynamicContainer):
    add_services_with_assigned_interface(container, interface=IApplicationService)
    
def add_domain_services(container: DynamicContainer):
    add_services_with_assigned_interface(container, interface=IDomainService)
    
def add_request_handlers(container: DynamicContainer):
    add_services_with_assigned_interface(container, interface=RequestHandler)

