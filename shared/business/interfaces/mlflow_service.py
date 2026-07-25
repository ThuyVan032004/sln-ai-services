from abc import ABC, abstractmethod


class IMlflowService(ABC):
    @abstractmethod
    def load_model(self, model_name: str, alias: str):
        pass
    
    