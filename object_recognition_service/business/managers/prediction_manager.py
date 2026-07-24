from data.entities.prediction import Prediction
from data.repository import ObjectRecognitionRepository
from dependency_injector.wiring import inject, Provide

from business.domain_service import ObjectRecognitionDomainService
from host.container import container

class PredictionManager(ObjectRecognitionDomainService):
    @inject
    def __init__(self, repository: ObjectRecognitionRepository[Prediction] = Provide[container.prediction_repository]):
        super().__init__(repository)