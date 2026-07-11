from datetime import datetime

from pydantic import BaseModel


class AuditModelBase(BaseModel):
    created_at: datetime
    last_updated_at: datetime
    deleted_at: datetime
    is_deleted: bool = False
    