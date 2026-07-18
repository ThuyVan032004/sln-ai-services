from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4

from shared.src.data.models.audit_model_base import AuditModelBase
from data.enums.model_enum import ModelStatus


class Model(AuditModelBase):
    __tablename__ = "model"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    checkpoint_uri: Mapped[str]
    status: Mapped[ModelStatus] = mapped_column(
        Enum(ModelStatus, name="status"),
        nullable=False,
    )