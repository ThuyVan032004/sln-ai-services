from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, Boolean, func
from sqlmodel import SQLModel, Field


class AuditModelBase(SQLModel):
    created_at: datetime = Field(
        sa_type=DateTime(timezone=True),
        sa_column_kwargs={"server_default": func.now()},
        nullable=False,
    )
    last_updated_at: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        nullable=True,
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        sa_type=DateTime(timezone=True),
        nullable=True,
    )
    is_deleted: bool = Field(
        default=False,
        sa_type=Boolean,
        sa_column_kwargs={"server_default": "false"},
        nullable=False,
    )