from uuid import UUID, uuid4
from sqlalchemy.orm import Mapped, mapped_column

from shared.src.data.models.audit_model_base import AuditModelBase


class Image(AuditModelBase):
    __tablename__ = "image"
    
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    file_name: Mapped[str]
    file_path: Mapped[str]
    file_size: Mapped[int]
    mime_type: Mapped[str]