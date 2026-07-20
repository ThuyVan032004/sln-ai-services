from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column

from shared.data.models.audit_model_base import AuditModelBase


class Prediction(AuditModelBase):
    __tablename__ = "prediction"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    image_id: Mapped[UUID]
    model_id: Mapped[UUID]
    category_id: Mapped[UUID]
    confidence: Mapped[float]
    bbox_x: Mapped[float]
    bbox_y: Mapped[float]
    bbox_width: Mapped[float]
    bbox_height: Mapped[float]