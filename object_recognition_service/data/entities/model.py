from sqlalchemy import Column, Enum
from uuid import UUID, uuid4

from sqlmodel import Field

from shared.data.models.audit_model_base import AuditModelBase
from object_recognition_service.data.enums.model_enum import ModelStatus


class Model(AuditModelBase, table=True):
    __tablename__ = "model"
    __table_args__ = {"keep_existing": True}

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    model_type: str  # recognition | detection
    object_class: str
    model_name: str
    status: ModelStatus = Field(
        sa_column=Column(Enum(ModelStatus, name="status"), nullable=False)
    )