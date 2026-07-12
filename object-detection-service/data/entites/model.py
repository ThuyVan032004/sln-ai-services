from sqlalchemy.orm import Mapped, mapped_column
from uuid import UUID, uuid4

from shared.src.data.models.audit_model_base import AuditModelBase


class Model(AuditModelBase):
    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)
    name: Mapped[str]
    checkpoint_uri: Mapped[str]
    status: Mapped[str]