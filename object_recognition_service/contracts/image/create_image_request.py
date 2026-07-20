from uuid import UUID

from fastapi import File, UploadFile

from shared.contracts.requests.create_request import CreateRequest, CreateResponse


class CreateImageRequest(CreateRequest):
    file: UploadFile = File(..., description="The image file to be uploaded.")
    
class CreateImageResponse(CreateResponse):
    id: UUID
    file_name: str
    file_path: str
    file_size: int
    mime_type: str