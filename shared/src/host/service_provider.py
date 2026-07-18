import importlib
import inspect
import os
import pkgutil
from typing import Type
from dependency_injector.containers import DynamicContainer
from dependency_injector.providers import Factory
from pydantic.alias_generators import to_snake

from shared.src.business.interfaces.application_service import IApplicationService
from shared.src.business.interfaces.domain_service import IDomainService
from shared.src.common.constants.env_constants import EnvConstants


def add_services_with_assigned_interface[T](container: DynamicContainer, interface: Type[T]):
    application_name = os.getenv(EnvConstants.APPLICATION_NAME)
    
    if application_name is None:
        raise ValueError(f"Environment variable '{EnvConstants.APPLICATION_NAME}' is not set.")
    
    application = importlib.import_module(application_name)
    
    modules = [
        importlib.import_module(module)
        for _, module, _ in pkgutil.walk_packages(application.__path__, prefix=f"{application_name}." )
    ]
    
    classes = {
        to_snake(obj.__name__): obj
        for module in modules
        for _, obj in inspect.getmembers(module, inspect.isclass)
        if issubclass(obj, interface) and obj is not interface and not inspect.isabstract(obj)
    }
    
    for class_name, cls in classes.items():
        setattr(container, class_name, Factory(cls))
        

def add_application_services(container: DynamicContainer):
    add_services_with_assigned_interface(container, interface=IApplicationService)
    
def add_domain_services(container: DynamicContainer):
    add_services_with_assigned_interface(container, interface=IDomainService)

