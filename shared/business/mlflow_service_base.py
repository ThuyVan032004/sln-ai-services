from asyncio.log import logger
import os
import mlflow

from shared.business.interfaces.mlflow_service import IMlflowService
from shared.common.constants.env_constants import EnvConstants


class MlflowServiceBase(IMlflowService):
    def __init__(self):
        self.dagshub_owner = os.environ[EnvConstants.DAGSHUB_OWNER]
        self.dagshub_repo = os.environ[EnvConstants.DAGSHUB_REPO]
        self.dagshub_username = os.environ[EnvConstants.DAGSHUB_USERNAME]
        self.dagshub_token = os.environ[EnvConstants.DAGSHUB_TOKEN]
        self.tracking_uri = f"https://dagshub.com/{self.dagshub_owner}/{self.dagshub_repo}.mlflow"
        
    def load_model(self, model_name: str, alias: str):
        mlflow.set_tracking_uri(self.tracking_uri)

        # DagsHub's MLflow server uses basic auth; MLflow reads these env vars.
        os.environ["MLFLOW_TRACKING_USERNAME"] = self.dagshub_username
        os.environ["MLFLOW_TRACKING_PASSWORD"] = self.dagshub_token
        
        model_uri = f"models:/{model_name}@{alias}"
        return mlflow.pyfunc.load_model(model_uri)