from typing import Optional
from uuid import UUID, uuid4

from sqlmodel import Field

from shared.data.models.audit_model_base import AuditModelBase


class Prediction(AuditModelBase, table=True):
    __tablename__ = "prediction"
    __table_args__ = {"keep_existing": True}

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    image_id: UUID
    detection_model_id: UUID
    recognition_model_id: UUID
    category_id: Optional[UUID] = None
    confidence: float
    bbox_x: float
    bbox_y: float
    bbox_width: float
    bbox_height: float