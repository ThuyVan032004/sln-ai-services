from uuid import UUID, uuid4
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column

from shared.src.data.models.audit_model_base import AuditModelBase
from data.enums.model_enum import ModelStatus


class Category(AuditModelBase):
    __tablename__ = "category"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    member: Mapped[str]
    label: Mapped[int]