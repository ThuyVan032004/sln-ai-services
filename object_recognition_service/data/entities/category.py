from uuid import UUID, uuid4
from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlmodel import Field

from shared.data.models.audit_model_base import AuditModelBase
from data.enums.model_enum import ModelStatus


class Category(AuditModelBase, table=True):
    __tablename__ = "category"
    __table_args__ = {"keep_existing": True}
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    object_class: str
    member: str
    label: int