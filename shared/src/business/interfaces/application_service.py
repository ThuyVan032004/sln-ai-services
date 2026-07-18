from abc import ABC, abstractmethod
from dependency_injector.providers import Provider

from shared.src.business.interfaces.domain_service import IDomainService
from shared.src.data.interfaces.repository import IRepository


class IApplicationService(ABC):
    pass