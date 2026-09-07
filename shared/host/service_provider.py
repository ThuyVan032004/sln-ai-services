import importlib
import inspect
import logging
import os
import pkgutil
from typing import Type, get_args, get_origin
from cqrs import RequestHandler, RequestMap
from dependency_injector.containers import DynamicContainer
from dependency_injector.providers import Factory
from pydantic.alias_generators import to_snake

from shared.business.interfaces import IApplicationService, IDomainService
from shared.common.constants import EnvConstants
from shared.business.interfaces import IMlflowService

logger = logging.getLogger(__name__)

def add_services_with_assigned_interface[T](container: DynamicContainer, interface: Type[T]):
    application_name = os.getenv(EnvConstants.APPLICATION_NAME)
    
    if application_name is None:
        raise ValueError(f"Environment variable '{EnvConstants.APPLICATION_NAME}' is not set.")
    
    application = importlib.import_module(application_name)
    
    modules = []
    for _, module_name, is_package in pkgutil.walk_packages(application.__path__, prefix=f"{application_name}."):
        parts = module_name.split(".")
        
        if "entities" in parts or is_package:
            continue
            
        try:
            modules.append(importlib.import_module(module_name))
        except Exception as e:
            logger.error(f"Cannot import module {module_name}: {e}")
    
    classes = {
        to_snake(obj.__name__): obj
        for module in modules
        for _, obj in inspect.getmembers(module, inspect.isclass)
        if issubclass(obj, interface) and obj is not interface and not inspect.isabstract(obj)
    }
    
    for class_name, cls in classes.items():
        logger.info(f"Registering {cls.__name__} as {class_name} in the container.")
        setattr(container, class_name, Factory(cls))
        
def add_request_handlers(
    container: DynamicContainer,
    request_map: RequestMap,
):
    application_name = os.getenv(EnvConstants.APPLICATION_NAME)

    if application_name is None:
        raise ValueError(f"Environment variable '{EnvConstants.APPLICATION_NAME}' is not set.")

    application = importlib.import_module(application_name)

    for _, module_name, is_package in pkgutil.walk_packages(
        application.__path__,
        prefix=f"{application_name}.",
    ):
        if "entities" in module_name.split(".") or is_package:
            continue

        module = importlib.import_module(module_name)

        for _, handler_cls in inspect.getmembers(module, inspect.isclass):
            if (
                issubclass(handler_cls, RequestHandler)
                and handler_cls is not RequestHandler
                and not inspect.isabstract(handler_cls)
            ):
                setattr(container, handler_cls.__name__, Factory(handler_cls))

                for base in getattr(handler_cls, "__orig_bases__", ()):
                    if get_origin(base) is RequestHandler:
                        request_type, _ = get_args(base)
                        request_map.bind(request_type, handler_cls)
                        break
                    

def add_application_services(container: DynamicContainer):
    add_services_with_assigned_interface(container, interface=IApplicationService)
    
def add_domain_services(container: DynamicContainer):
    add_services_with_assigned_interface(container, interface=IDomainService)

def add_mlflow_service(container: DynamicContainer):
    add_services_with_assigned_interface(container, interface=IMlflowService)

