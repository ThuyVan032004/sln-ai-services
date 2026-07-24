from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column
from sqlmodel import Field

from shared.data.models.audit_model_base import AuditModelBase


class Image(AuditModelBase, table=True):
    __tablename__ = "image"
    __table_args__ = {"keep_existing": True}
    
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    file_name: str
    file_path: str
    file_size: int
    mime_type: str