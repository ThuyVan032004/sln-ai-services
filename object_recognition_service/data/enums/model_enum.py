from enum import Enum


class ModelStatus(Enum):
    UPLOADING = "uploading"   # checkpoint being written/uploaded
    READY = "ready"           # available for use/inference
    FAILED = "failed"         # training/upload failed
    ARCHIVED = "archived"     # deprecated/retired, kept for history
    DELETED = "deleted"       # soft-deleted